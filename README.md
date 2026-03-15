# linkbreakers

Official Python SDK for the Linkbreakers API.

[![PyPI version](https://badge.fury.io/py/linkbreakers.svg)](https://pypi.org/project/linkbreakers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install linkbreakers
```

## Usage

### Synchronous Client

```python
from linkbreakers import LinkebreakersClient

# Create API client
with LinkebreakersClient(
    api_key='your_api_key_here',
    base_url='https://api.linkbreakers.com'
) as client:
    # Create a shortened link
    response = client.post('/api/v1/links', json={
        'destination': 'https://example.com',
        'name': 'My Link'
    })

    if response.is_success:
        link = response.json()
        print(f'Short link: {link["shortlink"]}')
    else:
        print(f'Error: {response.status_code}')

    # Get a link
    response = client.get(f'/api/v1/links/{link_id}')
    link = response.json()

    # Update a link
    response = client.patch(f'/api/v1/links/{link_id}', json={
        'name': 'Updated Name'
    })

    # Delete a link
    client.delete(f'/api/v1/links/{link_id}')
```

### Async Client

```python
from linkbreakers import AsyncLinkebreakersClient
import asyncio

async def main():
    async with AsyncLinkebreakersClient(
        api_key='your_api_key_here',
        base_url='https://api.linkbreakers.com'
    ) as client:
        # Create a shortened link
        response = await client.post('/api/v1/links', json={
            'destination': 'https://example.com',
            'name': 'My Async Link'
        })

        link = response.json()
        print(f'Short link: {link["shortlink"]}')

asyncio.run(main())
```

### Type-Safe Models

The SDK includes Pydantic models for all API types:

```python
from linkbreakers.models import CreateLinkRequest, Link

# Use models for type checking
request = CreateLinkRequest(
    destination='https://example.com',
    name='My Link'
)

response = client.post('/api/v1/links', json=request.dict())
```

## Features

- ✅ Full type hints and autocompletion support with Pydantic v2
- ✅ Synchronous and asynchronous clients
- ✅ Python 3.8+ support
- ✅ Auto-generated from OpenAPI specification
- ✅ Automatically updated when API changes
- ✅ Built on modern httpx library

## Documentation

For complete API documentation, visit [https://docs.linkbreakers.com](https://docs.linkbreakers.com)

## Auto-Generated SDK

This SDK is automatically generated from the Linkbreakers OpenAPI specification. When the API is updated, this SDK is automatically regenerated and published.

**Current API Version:** See [OPENAPI_VERSION](./OPENAPI_VERSION)

## Support

- **Issues:** [GitHub Issues](https://github.com/linkbreakers-com/linkbreakers-python/issues)
- **Documentation:** [https://docs.linkbreakers.com](https://docs.linkbreakers.com)

## License

MIT License - see [LICENSE](./LICENSE) for details.
