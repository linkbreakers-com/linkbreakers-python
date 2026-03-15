# linkbreakers

Official Python SDK for the Linkbreakers API.

[![PyPI version](https://badge.fury.io/py/linkbreakers.svg)](https://pypi.org/project/linkbreakers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install linkbreakers
```

## Usage

```python
from linkbreakers import Configuration, ApiClient, LinksApi

# Configure API client
configuration = Configuration(
    api_key={'ApiKeyAuth': 'your_api_key_here'},
    host='https://api.linkbreakers.com'
)

# Create API client
with ApiClient(configuration) as api_client:
    links_api = LinksApi(api_client)

    # Create a shortened link
    link = links_api.create_link({
        'destination': 'https://example.com',
        'name': 'My Link'
    })

    print(f'Short link: {link.shortlink}')
```

### Full API Support

The SDK provides type-safe methods for all API operations:

```python
from linkbreakers import Configuration, ApiClient, LinksApi

configuration = Configuration(
    api_key={'ApiKeyAuth': 'your_api_key_here'},
    host='https://api.linkbreakers.com'
)

with ApiClient(configuration) as api_client:
    links_api = LinksApi(api_client)

    # Get a link by ID
    link = links_api.get_link(id='link-id')

    # Update a link
    updated = links_api.update_link(
        id='link-id',
        update_link_request={
            'name': 'Updated Name'
        }
    )

    # Delete a link
    links_api.delete_link(id='link-id')

    # List links with filtering
    links = links_api.list_links(
        page_size=50,
        search='my-search',
        tags=['tag1', 'tag2']
    )
```

## Features

- ✅ Full type hints and autocompletion support
- ✅ Python 3.7+ support
- ✅ Auto-generated from OpenAPI specification
- ✅ Automatically updated when API changes

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
