"""
Create Link Example

This example demonstrates how to create shortened links with various options.

Use Cases:
- Create short links for marketing campaigns
- Generate trackable links for email campaigns
- Create QR codes for print materials
- Build dynamic links with custom domains
- Tag and organize links for analytics
"""

import os
from linkbreakers import (
    Configuration,
    ApiClient,
    LinksApi,
    CreateLinkRequest,
    CreateBulkLinksRequest
)


def create_basic_link():
    """Example 1: Create a basic shortened link"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        links_api = LinksApi(api_client)

        try:
            response = links_api.links_service_create(
                create_link_request=CreateLinkRequest(
                    destination='https://example.com/my-landing-page',
                    name='Landing Page Campaign'
                )
            )

            print('✓ Basic link created')
            print(f'  - Short URL: {response.link.shortlink}')
            print(f'  - Link ID: {response.link.id}')
            print(f'  - Destination: {response.link.destination}')

            return response.link

        except Exception as error:
            print(f'✗ Failed to create link: {error}')
            raise


def create_custom_link():
    """Example 2: Create a link with custom shortlink and tags"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        links_api = LinksApi(api_client)

        try:
            response = links_api.links_service_create(
                create_link_request=CreateLinkRequest(
                    destination='https://example.com/summer-sale',
                    name='Summer Sale 2024',

                    # Custom shortlink (must be unique in your workspace)
                    shortlink='summer2024',

                    # Tags for organization and filtering
                    tags=['campaign', 'summer', '2024', 'email'],

                    # Metadata for custom tracking (key-value pairs)
                    metadata={
                        'campaign_id': 'SUMMER_2024',
                        'utm_source': 'email',
                        'utm_medium': 'newsletter',
                        'utm_campaign': 'summer_sale'
                    }
                )
            )

            print('✓ Custom link created')
            print(f'  - Short URL: {response.link.shortlink}')
            print(f'  - Tags: {response.link.tags}')
            print(f'  - Metadata: {response.link.metadata}')

            return response.link

        except Exception as error:
            print(f'✗ Failed to create custom link: {error}')
            raise


def create_link_with_qr_code():
    """Example 3: Create a link with QR code"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        links_api = LinksApi(api_client)

        try:
            response = links_api.links_service_create(
                create_link_request=CreateLinkRequest(
                    destination='https://example.com/event-registration',
                    name='Event Registration QR Code',

                    # Wait for QR code to be generated before returning
                    wait_for_qrcode=True,

                    # Optional: Use a specific QR code template
                    # qrcode_template_id='your-template-uuid',

                    tags=['event', 'qr-code']
                )
            )

            print('✓ Link with QR code created')
            print(f'  - Short URL: {response.link.shortlink}')
            print(f'  - QR Code URL: {response.link.qrcode_signed_url}')
            print(f'  - QR Code Design ID: {response.link.qrcode_design_id}')

            return response.link

        except Exception as error:
            print(f'✗ Failed to create link with QR code: {error}')
            raise


def create_link_with_custom_domain():
    """Example 4: Create a link with custom domain"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        links_api = LinksApi(api_client)

        try:
            response = links_api.links_service_create(
                create_link_request=CreateLinkRequest(
                    destination='https://example.com/branded-content',
                    name='Branded Link',

                    # Use your custom domain (must be set up in Linkbreakers)
                    custom_domain_id='your-custom-domain-uuid',

                    shortlink='branded',

                    tags=['branded', 'custom-domain']
                )
            )

            print('✓ Branded link created')
            print(f'  - Short URL: {response.link.shortlink}')
            print(f'  - Custom Domain ID: {response.link.custom_domain_id}')

            return response.link

        except Exception as error:
            print(f'✗ Failed to create branded link: {error}')
            raise


def bulk_create_links():
    """Example 5: Bulk create multiple links"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        links_api = LinksApi(api_client)

        links_to_create = [
            CreateLinkRequest(
                destination='https://example.com/product-1',
                name='Product 1',
                tags=['product', 'catalog'],
                metadata={'sku': 'PROD-001'}
            ),
            CreateLinkRequest(
                destination='https://example.com/product-2',
                name='Product 2',
                tags=['product', 'catalog'],
                metadata={'sku': 'PROD-002'}
            ),
            CreateLinkRequest(
                destination='https://example.com/product-3',
                name='Product 3',
                tags=['product', 'catalog'],
                metadata={'sku': 'PROD-003'}
            )
        ]

        try:
            response = links_api.links_service_create_bulk(
                create_bulk_links_request=CreateBulkLinksRequest(
                    links=links_to_create
                )
            )

            print(f'✓ Bulk created {len(response.links)} links')
            for link in response.links:
                print(f'  - {link.name}: {link.shortlink}')

            return response.links

        except Exception as error:
            print(f'✗ Failed to bulk create links: {error}')
            raise


if __name__ == '__main__':
    try:
        print('=== Create Link Examples ===\n')

        print('1. Basic Link:')
        create_basic_link()

        print('\n2. Custom Link with Tags:')
        create_custom_link()

        print('\n3. Link with QR Code:')
        create_link_with_qr_code()

        print('\n4. Bulk Create Links:')
        bulk_create_links()

        print('\n✓ All examples completed successfully')
    except Exception as error:
        print(f'\n✗ Examples failed: {error}')
        exit(1)
