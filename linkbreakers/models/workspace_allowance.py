# coding: utf-8

"""
    Linkbreakers API

    The Linkbreakers REST API: links, QR codes, workflows, visitors and analytics, as JSON over HTTPS. Send a workspace API token as `Authorization: Bearer <token>`.  ## Entry points  `GET https://api.linkbreakers.com/` and `GET https://api.linkbreakers.com/v1` answer without credentials with the API's name, version and links. This document is served at `https://api.linkbreakers.com/openapi.json`.  ## Rate limits  Every response describes where the caller stands in the IETF `RateLimit-Policy` and `RateLimit` header fields (draft-ietf-httpapi-ratelimit-headers), and in `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` and `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (a Unix timestamp) for clients that read those. A request past the limit gets `429 Too Many Requests` with `Retry-After` in seconds.  - Workspace API token: 720 requests per 60 seconds, per token. - Dashboard session or OAuth token: 600 requests per 60 seconds, per token. - No credentials: 300 requests per 60 seconds, per client IP.  Each plan also includes a number of API calls per billing cycle. Past it, calls answer `429` with the code `MAX_PUBLIC_API_QUERIED_REACHED` until the cycle renews or the plan changes.  ## Pagination  Every list pages with opaque cursors (AIP-158). Pass `pageSize`, then send the `nextPageToken` of each response back as `pageToken` (or its alias `cursor`) to get the next page. An empty or absent `nextPageToken` means the list is complete. Each list operation describes this in `x-pagination`.  ## Batches and background jobs  `POST /v1/links/bulk` creates up to 250 links in one transactional request; `POST /v1/links/batch` takes the same links as a bare JSON array. `POST /v1/links/bulk/jobs` accepts the same batch and answers `202 Accepted` at once with a job and a `Location` header; poll `GET /v1/jobs/{id}` until `status` is `JOB_STATUS_SUCCEEDED` (the created link ids are in `linksBulkCreate.linkIds`) or `JOB_STATUS_FAILED` (`error` says why, and nothing was created). Jobs can be read for 24 hours after they finish.  ## Paused workspaces  A free workspace whose members have not verified any email address is paused 7 days after sign-up. Its calls then answer `403` with the code `WORKSPACE_UNVERIFIED` and change nothing; QR codes and links keep working for visitors. To lift the pause, ask the workspace owner to verify their email: `POST /v1/members/email-verification` sends the verification email again, and works while the workspace is paused. `unverifiedPauseAt` on the workspace says when the pause starts.  ## Versioning and deprecation  The version is in the path: every operation lives under `/v1`. Within a version, changes are additive only: new operations, new optional request fields, new response fields and new enum values. Clients should ignore fields and enum values they do not know. Anything that would break an existing client ships under a new path version instead.  An operation is retired in two steps. First it is deprecated: it keeps working, is flagged `deprecated: true` in this document, and every response carries a `Deprecation` header field (RFC 9745) with the time it was deprecated and a `Link` with `rel=\"deprecation\"` to the policy. Then, at least 180 days later, it may be removed; that date is announced in advance in a `Sunset` header field (RFC 8594) and as `x-sunset` on the operation. The full policy: https://linkbreakers.com/help/article/api-versioning-and-deprecation-policy  A renamed operation keeps answering its former path while clients still call it, until that path's sunset at the latest: a former path no client calls for 14 days is removed. Responses on a former path carry the same `Deprecation`, `Sunset` and `Link` header fields; this document lists only the current path, and the policy lists the former paths that still answer.  ## Idempotent retries  Every POST, PUT and PATCH accepts an optional `Idempotency-Key` header (draft-ietf-httpapi-idempotency-key-header). Send a new unique value, such as a UUID, with each logical request and reuse it only to retry that request. A retry with the same key and the same request returns the first response, marked `Idempotent-Replayed: true`, instead of running again. Keys are scoped to the token and kept for 24 hours. The same key with a different request is refused with `422`, and a retry while the first request is still running gets `409` with `Retry-After`. Server errors (5xx) and refusals such as 401, 403 and 429 are not stored, so retrying them runs the request again.  ## Identifying your client  Send a `Linkbreakers-Client` request header saying which client made the call: `<client>/<version> (<details>)`, for example `my-integration/1.2.0 (python 3.12; linux)`. The official SDKs, the CLI and the MCP bridge set it for you, as `sdk-python/2.3.1 (python 3.12.4; linux)` or `cli/1.4.0 (darwin arm64)`. It is optional and changes nothing about how a request is handled; it tells us which clients and versions are in use, so we know what can be retired and what to fix first. Keep the details short and free of personal data. Browsers may send it too: it is allowed by CORS.

    The version of the OpenAPI document: 1.202.0
    Contact: support@linkbreakers.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from linkbreakers.models.type_date import TypeDate
from typing import Optional, Set
from typing_extensions import Self

class WorkspaceAllowance(BaseModel):
    """
    One limit the workspace's plan sets, with what the workspace has used of it.
    """ # noqa: E501
    cheapest_action_cost: Optional[StrictInt] = Field(default=None, alias="cheapestActionCost")
    cycle_end_at: Optional[datetime] = Field(default=None, description="The last second of the current cycle; the allowance refills one second later. Absent for totals that never refill and when nothing has been counted yet.", alias="cycleEndAt")
    cycle_start_at: Optional[datetime] = Field(default=None, description="Start of the current cycle. Absent when nothing has been counted yet.", alias="cycleStartAt")
    key: Optional[StrictStr] = Field(default=None, description="- PLAN_LIMIT_KEY_UNSPECIFIED: Not set  - PLAN_LIMIT_KEY_CUSTOM_DOMAINS: Custom domains connected to the workspace  - PLAN_LIMIT_KEY_TEAM_MEMBERS: Members of the workspace  - PLAN_LIMIT_KEY_PLATFORM_CREDITS: Platform credits, spent by creating links and by AI features  - PLAN_LIMIT_KEY_TRACKED_VISITS: Tracked visits (scans and clicks)  - PLAN_LIMIT_KEY_PUBLIC_API_CALLS: Public API calls  - PLAN_LIMIT_KEY_WEBHOOKS: Webhooks configured in the workspace  - PLAN_LIMIT_KEY_ASSISTANT_MESSAGES_PER_MINUTE: Assistant messages per minute  - PLAN_LIMIT_KEY_LINKS_INCLUDED: Links the monthly platform credits pay for. Links are not capped on their own: each one spends credits.  - PLAN_LIMIT_KEY_MEDIA_STORAGE_MB: Megabytes of uploaded media (media for Open media steps, QR code logos, page theme images) the workspace may hold at once. A standing total: deleting media frees it.")
    kind: Optional[StrictStr] = Field(default=None, description="- PLAN_LIMIT_KIND_UNSPECIFIED: Not set  - PLAN_LIMIT_KIND_TOTAL: A standing total that does not refill, such as connected domains  - PLAN_LIMIT_KIND_MONTHLY: An allowance that refills every month  - PLAN_LIMIT_KIND_PER_MINUTE: A rate that refills every minute  - PLAN_LIMIT_KIND_UNLIMITED: No ceiling  - PLAN_LIMIT_KIND_METERED: No ceiling; every unit is billed")
    limit: Optional[StrictInt] = Field(default=None, description="The ceiling. Absent when kind is PLAN_LIMIT_KIND_UNLIMITED or PLAN_LIMIT_KIND_METERED.")
    limit_bytes: Optional[StrictInt] = Field(default=None, description="Media storage only: the most media the workspace may hold, in bytes. Absent for other limits and when there is no ceiling.", alias="limitBytes")
    locked_count: Optional[StrictInt] = Field(default=None, description="Tracked visits only: visits recorded past the limit in the current cycle that the workspace's plan still locks. Absent for other limits.", alias="lockedCount")
    locked_total_count: Optional[StrictInt] = Field(default=None, description="Tracked visits only: every visit the workspace's plan still locks, across all cycles. Upgrading to a plan with a higher limit reveals them. Absent for other limits.", alias="lockedTotalCount")
    notice_dismissed: Optional[StrictBool] = Field(default=None, alias="noticeDismissed")
    reached: Optional[StrictBool] = Field(default=None, description="Whether the limit is used up for the current cycle. Platform credits count as reached once neither the monthly credits nor the purchased top-up credits hold cheapestActionCost, so nothing that spends credits can run. Never reached on a plan billed per unit used.")
    recorded_count: Optional[StrictInt] = Field(default=None, description="Tracked visits only: every visit recorded in the current cycle, used plus lockedCount. Absent for other limits.", alias="recordedCount")
    remaining: Optional[StrictInt] = Field(default=None, description="Units left in the current cycle. For platform credits, the monthly credits left plus the purchased top-up credits left. Absent when there is no ceiling.")
    resets_on: Optional[TypeDate] = Field(default=None, description="The day the allowance refills, which is the first day of the next cycle in the workspace's timezone. Absent for totals that never refill and when nothing has been counted yet.", alias="resetsOn")
    used: Optional[StrictInt] = Field(default=None, description="Units used in the current cycle. For a total such as custom domains, what the workspace holds.")
    used_bytes: Optional[StrictInt] = Field(default=None, description="Media storage only: the bytes the workspace's media holds, exact. used is the same figure in megabytes, rounded up. Absent for other limits.", alias="usedBytes")
    __properties: ClassVar[List[str]] = ["cheapestActionCost", "cycleEndAt", "cycleStartAt", "key", "kind", "limit", "limitBytes", "lockedCount", "lockedTotalCount", "noticeDismissed", "reached", "recordedCount", "remaining", "resetsOn", "used", "usedBytes"]

    @field_validator('key')
    def key_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['PLAN_LIMIT_KEY_UNSPECIFIED', 'PLAN_LIMIT_KEY_CUSTOM_DOMAINS', 'PLAN_LIMIT_KEY_TEAM_MEMBERS', 'PLAN_LIMIT_KEY_PLATFORM_CREDITS', 'PLAN_LIMIT_KEY_TRACKED_VISITS', 'PLAN_LIMIT_KEY_PUBLIC_API_CALLS', 'PLAN_LIMIT_KEY_WEBHOOKS', 'PLAN_LIMIT_KEY_ASSISTANT_MESSAGES_PER_MINUTE', 'PLAN_LIMIT_KEY_LINKS_INCLUDED', 'PLAN_LIMIT_KEY_MEDIA_STORAGE_MB']):
            raise ValueError("must be one of enum values ('PLAN_LIMIT_KEY_UNSPECIFIED', 'PLAN_LIMIT_KEY_CUSTOM_DOMAINS', 'PLAN_LIMIT_KEY_TEAM_MEMBERS', 'PLAN_LIMIT_KEY_PLATFORM_CREDITS', 'PLAN_LIMIT_KEY_TRACKED_VISITS', 'PLAN_LIMIT_KEY_PUBLIC_API_CALLS', 'PLAN_LIMIT_KEY_WEBHOOKS', 'PLAN_LIMIT_KEY_ASSISTANT_MESSAGES_PER_MINUTE', 'PLAN_LIMIT_KEY_LINKS_INCLUDED', 'PLAN_LIMIT_KEY_MEDIA_STORAGE_MB')")
        return value

    @field_validator('kind')
    def kind_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['PLAN_LIMIT_KIND_UNSPECIFIED', 'PLAN_LIMIT_KIND_TOTAL', 'PLAN_LIMIT_KIND_MONTHLY', 'PLAN_LIMIT_KIND_PER_MINUTE', 'PLAN_LIMIT_KIND_UNLIMITED', 'PLAN_LIMIT_KIND_METERED']):
            raise ValueError("must be one of enum values ('PLAN_LIMIT_KIND_UNSPECIFIED', 'PLAN_LIMIT_KIND_TOTAL', 'PLAN_LIMIT_KIND_MONTHLY', 'PLAN_LIMIT_KIND_PER_MINUTE', 'PLAN_LIMIT_KIND_UNLIMITED', 'PLAN_LIMIT_KIND_METERED')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of WorkspaceAllowance from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of resets_on
        if self.resets_on:
            _dict['resetsOn'] = self.resets_on.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorkspaceAllowance from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "cheapestActionCost": obj.get("cheapestActionCost"),
            "cycleEndAt": obj.get("cycleEndAt"),
            "cycleStartAt": obj.get("cycleStartAt"),
            "key": obj.get("key"),
            "kind": obj.get("kind"),
            "limit": obj.get("limit"),
            "limitBytes": obj.get("limitBytes"),
            "lockedCount": obj.get("lockedCount"),
            "lockedTotalCount": obj.get("lockedTotalCount"),
            "noticeDismissed": obj.get("noticeDismissed"),
            "reached": obj.get("reached"),
            "recordedCount": obj.get("recordedCount"),
            "remaining": obj.get("remaining"),
            "resetsOn": TypeDate.from_dict(obj["resetsOn"]) if obj.get("resetsOn") is not None else None,
            "used": obj.get("used"),
            "usedBytes": obj.get("usedBytes")
        })
        return _obj


