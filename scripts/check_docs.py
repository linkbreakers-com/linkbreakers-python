"""Checks the README snippets and examples against the installed SDK.

The READMEs and examples are written by hand and survive regeneration, so
nothing else ties them to the generated client. This walks every Python block
in README.md and examples/README.md and every examples/*.py file, and fails
when one imports a name the package does not export, calls a method an API
class does not have, passes a keyword the method or model does not accept, or
reads a field a response model does not have.
"""

import ast
import importlib
import inspect
import re
import sys
import typing
from pathlib import Path

from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
DOCS = ["README.md", "examples/README.md"]
BLOCK = re.compile(r"```python\n(.*?)```", re.S)


def model_of(annotation):
    """The model an annotation holds, looking through Optional and List."""
    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return annotation
    for arg in typing.get_args(annotation):
        model = model_of(arg)
        if model is not None:
            return model
    return None


def field_names(model):
    names = set(model.model_fields)
    names.update(f.alias for f in model.model_fields.values() if f.alias)
    return names


def accepted_keywords(func):
    try:
        params = inspect.signature(func).parameters.values()
    except (TypeError, ValueError):
        return None
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params):
        return None
    return {p.name for p in params}


def return_model(func):
    try:
        hints = typing.get_type_hints(inspect.unwrap(func))
    except Exception:
        return None
    return model_of(hints.get("return"))


class Checker(ast.NodeVisitor):
    def __init__(self, source):
        self.source = source
        self.names = {}
        self.types = {}
        self.errors = []

    def fail(self, node, message):
        self.errors.append(f"{self.source}:{node.lineno}: {message}")

    def visit_ImportFrom(self, node):
        if node.module and node.module.split(".")[0] == "linkbreakers":
            module = importlib.import_module(node.module)
            for alias in node.names:
                if not hasattr(module, alias.name):
                    self.fail(node, f"{node.module} has no {alias.name}")
                else:
                    self.names[alias.asname or alias.name] = getattr(module, alias.name)
        self.generic_visit(node)

    def type_of(self, node):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and inspect.isclass(self.names.get(func.id)):
                return self.names[func.id]
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                owner = self.types.get(func.value.id)
                method = getattr(owner, func.attr, None) if owner else None
                if method is not None:
                    return return_model(method)
        if isinstance(node, ast.Attribute):
            owner = self.type_of(node.value)
            if owner is not None and issubclass(owner, BaseModel):
                field = owner.model_fields.get(node.attr)
                return model_of(field.annotation) if field else None
        if isinstance(node, ast.Name):
            return self.types.get(node.id)
        return None

    def visit_Assign(self, node):
        self.generic_visit(node)
        kind = self.type_of(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                if kind is None:
                    self.types.pop(target.id, None)
                else:
                    self.types[target.id] = kind

    def visit_For(self, node):
        kind = self.type_of(node.iter)
        if isinstance(node.target, ast.Name) and kind is not None:
            self.types[node.target.id] = kind
        self.generic_visit(node)

    def visit_With(self, node):
        for item in node.items:
            if isinstance(item.optional_vars, ast.Name):
                kind = self.type_of(item.context_expr)
                if kind is not None:
                    self.types[item.optional_vars.id] = kind
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        target = None
        if isinstance(func, ast.Name) and inspect.isclass(self.names.get(func.id)):
            cls = self.names[func.id]
            if issubclass(cls, BaseModel):
                allowed = field_names(cls)
                for keyword in node.keywords:
                    if keyword.arg and keyword.arg not in allowed:
                        self.fail(node, f"{cls.__name__} has no field {keyword.arg}")
        elif isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            owner = self.types.get(func.value.id)
            if owner is not None and not issubclass(owner, BaseModel):
                target = getattr(owner, func.attr, None)
                if target is None:
                    self.fail(node, f"{owner.__name__} has no method {func.attr}")
                else:
                    allowed = accepted_keywords(target)
                    for keyword in node.keywords:
                        if allowed is not None and keyword.arg and keyword.arg not in allowed:
                            self.fail(node, f"{owner.__name__}.{func.attr} takes no argument {keyword.arg}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.ctx, ast.Load):
            owner = self.type_of(node.value)
            if owner is not None and issubclass(owner, BaseModel):
                aliases = {f.alias: name for name, f in owner.model_fields.items() if f.alias}
                if node.attr not in owner.model_fields and node.attr in aliases:
                    self.fail(node, f"{owner.__name__}.{node.attr} is the JSON name, the attribute is {aliases[node.attr]}")
                elif node.attr not in owner.model_fields and not hasattr(owner, node.attr):
                    self.fail(node, f"{owner.__name__} has no field {node.attr}")
        self.generic_visit(node)


def sources():
    for doc in DOCS:
        blocks = BLOCK.findall((ROOT / doc).read_text())
        yield doc, "\n".join(blocks)
    for example in sorted((ROOT / "examples").glob("*.py")):
        yield str(example.relative_to(ROOT)), example.read_text()


def main():
    errors = []
    checked = 0
    for name, code in sources():
        checker = Checker(name)
        checker.visit(ast.parse(code, filename=name))
        errors.extend(checker.errors)
        checked += 1
    if errors:
        print("\n".join(errors))
        print("\nA README snippet or example no longer matches the generated SDK.")
        return 1
    print(f"Checked {checked} documents against the installed linkbreakers package.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
