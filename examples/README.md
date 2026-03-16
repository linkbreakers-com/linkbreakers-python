# Linkbreakers Python SDK Examples

Complete, runnable examples for common use cases with the Linkbreakers API.

## Prerequisites

```bash
# Install the SDK
pip install linkbreakers

# Set your API key
export LINKBREAKERS_API_KEY='your-api-key-here'
```

Or create a `.env` file (see [.env.example](../.env.example)):

```bash
LINKBREAKERS_API_KEY=your-api-key-here
```

## Running Examples

Each example can be run directly with Python:

```bash
python examples/identify_visitor.py
```

## Examples

### 🎯 Visitor Management

#### [identify_visitor.py](./identify_visitor.py)
**Most Important Use Case** - Identify or create a visitor using their LBID from tracking.

```python
# Find or create visitor, merge attributes
response = visitors_api.visitors_service_identify(
    identify_request=IdentifyRequest(
        lbid='visitor-lbid-from-tracking',
        visitor=VisitorInput(
            data={
                '$email': 'user@example.com',
                '$phone': '+1234567890',
                'company': 'Acme Corp',
                'plan': 'premium'
            }
        )
    )
)
```

**When to use:**
- User signs up or logs in
- User fills out a form
- Capturing visitor information from tracking events
- First-time visitor identification

**Key concepts:**
- Uses LBID (base64 encoded event ID from click/scan)
- Creates visitor if doesn't exist, updates if exists
- System fields use `$` prefix (`$email`, `$phone`, `$firstName`, `$lastName`)
- Custom attributes have no prefix
- `set_once=True` prevents overwriting existing data

---

#### [update_visitor.py](./update_visitor.py)
Update an existing visitor using their UUID.

```python
# Update visitor by UUID
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

**When to use:**
- User updates their profile
- Subscription changes
- Enriching data from external sources
- You have the visitor UUID from your database

**Includes:**
- Single visitor update
- Batch update multiple visitors

---

#### [list_visitors.py](./list_visitors.py)
Query, filter, and search visitors.

```python
# List with filters
visitors = visitors_api.visitors_service_list(
    page_size=50,
    email='user@example.com',
    link_id='link-uuid',
    search='Acme Corp'
)
```

**Features:**
- Pagination through results
- Filter by email (exact match)
- Filter by link ID
- Fuzzy search across fields
- Export to CSV
- Include related data (devices, events, links)

---

### 🔗 Link Management

#### [create_link.py](./create_link.py)
Create shortened links with various configurations.

```python
# Basic link
link = links_api.links_service_create(
    create_link_request=CreateLinkRequest(
        destination='https://example.com',
        name='My Campaign'
    )
)

# With custom shortlink, tags, and metadata
custom_link = links_api.links_service_create(
    create_link_request=CreateLinkRequest(
        destination='https://example.com/sale',
        shortlink='summer2024',
        tags=['campaign', 'summer'],
        metadata={
            'campaign_id': 'SUMMER_2024'
        }
    )
)
```

**Includes examples for:**
- Basic shortened links
- Custom shortlinks
- Tags and metadata
- QR code generation
- Custom domains
- Bulk link creation

---

## Key Concepts

### LBID vs UUID

- **LBID** (Linkbreakers ID): Base64 encoded event ID from click/scan tracking
  - Comes from tracking cookies, query parameters, or webhooks
  - Used with `identify` endpoint
  - Format: `ZXhhbXBsZS1saW5rYnJlYWtlcnMtaWQtMTIzNDU2Nzg5MA==`

- **UUID**: Standard visitor identifier stored in your database
  - Returned from API responses
  - Used with `update`, `get`, `delete` endpoints
  - Format: `550e8400-e29b-41d4-a716-446655440000`

### System Fields vs Custom Attributes

**System fields** (prefixed with `$`):
- `$email` - Email address
- `$phone` - Phone number
- `$firstName` - First name
- `$lastName` - Last name

**Custom attributes** (no prefix):
- Store any data you need: `company`, `plan`, `signupDate`, etc.
- Used for segmentation, personalization, and analytics

### Pagination

Most list endpoints support pagination:

```python
page_token = None

while True:
    response = api.list(
        page_size=200,
        page_token=page_token
    )

    # Process results

    page_token = response.next_page_token
    if not page_token:
        break
```

## Common Patterns

### Error Handling

```python
try:
    visitor = visitors_api.visitors_service_identify(
        identify_request=IdentifyRequest(...)
    )
    print('Success:', visitor)
except ApiException as error:
    print(f'API Error: {error.status} - {error.reason}')
except Exception as error:
    print(f'Error: {error}')
```

### Environment Configuration

```python
import os
from linkbreakers import Configuration, ApiClient

configuration = Configuration(
    access_token=os.getenv('LINKBREAKERS_API_KEY'),
    host=os.getenv('LINKBREAKERS_API_URL', 'https://api.linkbreakers.com')
)

with ApiClient(configuration) as api_client:
    # Use api_client
    pass
```

### Context Manager

Always use the `with` statement for ApiClient to ensure proper resource cleanup:

```python
with ApiClient(configuration) as api_client:
    api = SomeApi(api_client)
    result = api.some_method()
    # Resources are automatically cleaned up
```

## Need Help?

- **API Documentation:** https://linkbreakers.com/help/api
- **SDK Issues:** https://github.com/linkbreakers-com/linkbreakers-python/issues
- **Main README:** [../README.md](../README.md)

## Contributing Examples

Have a useful example? Submit a PR!

1. Create a new file in `examples/`
2. Include clear docstrings and comments
3. Make it runnable with realistic fake data
4. Add it to this README
