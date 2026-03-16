"""
List Visitors Example

This example demonstrates how to query and filter visitors.

Use Cases:
- Export visitor data for analysis
- Find visitors by email or attributes
- Build customer segments
- Search for specific visitors
- Paginate through large visitor lists
"""

import os
from linkbreakers import (
    Configuration,
    ApiClient,
    VisitorsApi
)


def list_all_visitors():
    """Example 1: List all visitors with pagination"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        try:
            response = visitors_api.visitors_service_list(
                page_size=50,  # Max: 200
                # page_token='next-page-token',  # For pagination
            )

            print('✓ Retrieved visitors')
            print(f'  - Total in this page: {len(response.visitors) if response.visitors else 0}')
            print(f'  - Next page token: {response.next_page_token or "None (last page)"}')

            if response.visitors:
                for visitor in response.visitors:
                    email = visitor.email or 'Anonymous'
                    print(f'\n  Visitor: {email}')
                    print(f'    - ID: {visitor.id}')
                    print(f'    - Name: {visitor.first_name} {visitor.last_name}')
                    print(f'    - Phone: {visitor.phone or "N/A"}')

            return response

        except Exception as error:
            print(f'✗ Failed to list visitors: {error}')
            raise


def find_visitor_by_email(email):
    """Example 2: Find a visitor by email"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        try:
            response = visitors_api.visitors_service_list(
                email=email,  # Exact match filter
                page_size=1
            )

            if response.visitors and len(response.visitors) > 0:
                visitor = response.visitors[0]
                print('✓ Found visitor')
                print(f'  - ID: {visitor.id}')
                print(f'  - Email: {visitor.email}')
                print(f'  - Attributes: {visitor.attributes}')
                return visitor
            else:
                print(f'✗ No visitor found with email: {email}')
                return None

        except Exception as error:
            print(f'✗ Failed to find visitor: {error}')
            raise


def search_visitors(query):
    """Example 3: Search visitors across fields"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        try:
            response = visitors_api.visitors_service_list(
                search=query,  # Fuzzy search across name, email, attributes
                page_size=50
            )

            visitor_count = len(response.visitors) if response.visitors else 0
            print(f'✓ Search results for "{query}"')
            print(f'  - Found {visitor_count} visitors')

            if response.visitors:
                for visitor in response.visitors:
                    email = visitor.email or 'Anonymous'
                    print(f'\n  {email}')
                    print(f'    Name: {visitor.first_name} {visitor.last_name}')
                    company = visitor.attributes.get('company') if visitor.attributes else None
                    print(f'    Company: {company or "N/A"}')

            return response.visitors

        except Exception as error:
            print(f'✗ Search failed: {error}')
            raise


def get_visitors_by_link(link_id):
    """Example 4: Get visitors who clicked a specific link"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        try:
            response = visitors_api.visitors_service_list(
                link_id=link_id,  # Filter by link UUID
                page_size=100,
                include=['events']  # Include event data
            )

            visitor_count = len(response.visitors) if response.visitors else 0
            print(f'✓ Visitors who clicked link {link_id}')
            print(f'  - Total visitors: {visitor_count}')

            if response.visitors:
                for visitor in response.visitors:
                    email = visitor.email or 'Anonymous'
                    event_count = len(visitor.events) if visitor.events else 0
                    print(f'\n  {email}')
                    print(f'    Events: {event_count}')

            return response.visitors

        except Exception as error:
            print(f'✗ Failed to get visitors by link: {error}')
            raise


def get_all_visitors_paginated():
    """Example 5: Paginate through all visitors"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        all_visitors = []
        page_token = None
        page_num = 1

        try:
            while True:
                print(f'Fetching page {page_num}...')

                response = visitors_api.visitors_service_list(
                    page_size=200,  # Max page size
                    page_token=page_token
                )

                if response.visitors:
                    all_visitors.extend(response.visitors)
                    print(f'  ✓ Retrieved {len(response.visitors)} visitors')

                page_token = response.next_page_token
                page_num += 1

                # Break if no more pages
                if not page_token:
                    break

                # Optional: Add delay to avoid rate limits
                import time
                time.sleep(0.1)

            print(f'\n✓ Retrieved all {len(all_visitors)} visitors')
            return all_visitors

        except Exception as error:
            print(f'✗ Failed to paginate visitors: {error}')
            raise


def export_visitors_to_csv():
    """Example 6: Export visitors to CSV"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        try:
            response = visitors_api.visitors_service_list(
                page_size=200,
                response_format='RESPONSE_FORMAT_CSV'
            )

            print('✓ Exported visitors to CSV')
            print(f'  - CSV data length: {len(response.csv) if response.csv else 0}')

            # Save to file
            from datetime import date
            filename = f'visitors-export-{date.today()}.csv'
            with open(filename, 'w') as f:
                f.write(response.csv)
            print(f'  - Saved to: {filename}')

            return response.csv

        except Exception as error:
            print(f'✗ Failed to export visitors: {error}')
            raise


if __name__ == '__main__':
    try:
        print('=== List Visitors Examples ===\n')

        print('1. List All Visitors:')
        list_all_visitors()

        print('\n2. Find Visitor by Email:')
        find_visitor_by_email('john.doe@example.com')

        print('\n3. Search Visitors:')
        search_visitors('Acme')

        print('\n✓ All examples completed successfully')
    except Exception as error:
        print(f'\n✗ Examples failed: {error}')
        exit(1)
