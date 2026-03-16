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

### Identifying Visitors

Use the `VisitorsApi` to identify and update visitor profiles. The `identify` method finds or creates a visitor using their LBID (from tracking) and merges attributes:

```python
from linkbreakers import (
    Configuration,
    ApiClient,
    VisitorsApi,
    IdentifyRequest,
    VisitorInput
)

configuration = Configuration(
    access_token='your_api_key_here',
    host='https://api.linkbreakers.com'
)

with ApiClient(configuration) as api_client:
    visitors_api = VisitorsApi(api_client)

    # Identify a visitor using their LBID (from tracking cookie/parameter)
    response = visitors_api.visitors_service_identify(
        identify_request=IdentifyRequest(
            lbid='visitor-lbid-from-tracking',  # Base64 encoded event ID from click/scan
            visitor=VisitorInput(
                data={
                    # System fields (prefixed with "$")
                    '$email': 'user@example.com',
                    '$phone': '+1234567890',
                    '$firstName': 'John',
                    '$lastName': 'Doe',

                    # Custom attributes (no "$" prefix)
                    'company': 'Acme Corp',
                    'plan': 'premium',
                    'signupDate': '2024-01-01'
                }
            ),
            set_once=False  # If True, only sets empty fields (won't overwrite existing)
        )
    )

    print(f'Created new profile: {response.created}')
    print(f'Visitor: {response.visitor}')
```

**Update an existing visitor by UUID:**

```python
from linkbreakers import VisitorsServiceUpdateBody, VisitorInput

with ApiClient(configuration) as api_client:
    visitors_api = VisitorsApi(api_client)

    # When you have the visitor's UUID (from your database)
    visitor = visitors_api.visitors_service_update(
        id='visitor-uuid',
        visitors_service_update_body=VisitorsServiceUpdateBody(
            visitor=VisitorInput(
                data={
                    '$email': 'updated@example.com',
                    'plan': 'enterprise'
                }
            )
        )
    )
```

**Get visitor details:**

```python
with ApiClient(configuration) as api_client:
    visitors_api = VisitorsApi(api_client)

    visitor = visitors_api.visitors_service_get(
        id='visitor-uuid',
        include=['devices', 'events', 'links']  # Optional: include related data
    )
```

**List visitors:**

```python
with ApiClient(configuration) as api_client:
    visitors_api = VisitorsApi(api_client)

    visitors = visitors_api.visitors_service_list(
        page_size=50,
        email='user@example.com',  # Optional filters
        link_id='link-uuid',
        search='Acme Corp'
    )
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
