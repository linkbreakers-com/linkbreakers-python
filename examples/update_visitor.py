"""
Update Visitor Example

This example demonstrates how to update an existing visitor using their UUID.
Use this when you have the visitor's UUID from your database or a previous API call.

Difference from identify:
- identify: Uses LBID (from tracking) - finds OR creates visitor
- update: Uses UUID (from database) - only updates existing visitor

Use Cases:
- User updates their profile information
- User upgrades/downgrades their subscription
- Scheduled job enriches visitor data from external sources
- Real-time updates based on user actions in your app
"""

import os
from datetime import datetime
from linkbreakers import (
    Configuration,
    ApiClient,
    VisitorsApi,
    VisitorsServiceUpdateBody,
    VisitorInput
)


def update_visitor():
    """Update an existing visitor by UUID"""

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        # Visitor UUID
        #
        # This comes from:
        # 1. Your database (stored when you first identified the visitor)
        # 2. Previous API response (from identify or get visitor)
        # 3. Webhook payload
        #
        # Format: Standard UUID (e.g., "550e8400-e29b-41d4-a716-446655440000")
        visitor_id = '550e8400-e29b-41d4-a716-446655440000'

        try:
            visitor = visitors_api.visitors_service_update(
                id=visitor_id,
                visitors_service_update_body=VisitorsServiceUpdateBody(
                    visitor=VisitorInput(
                        data={
                            # Update system fields
                            '$email': 'john.doe.updated@example.com',
                            '$phone': '+14155559999',

                            # Update custom attributes
                            'plan': 'enterprise',
                            'planUpgradedAt': datetime.now().isoformat(),
                            'mrr': 499,
                            'seats': 10,
                            'lastActivity': datetime.now().isoformat(),

                            # Add new custom attributes
                            'customDomain': 'acme.example.com',
                            'ssoEnabled': True
                        }
                    )
                )
            )

            print('✓ Visitor updated successfully')
            print(f'  - Visitor ID: {visitor.id}')
            print(f'  - Email: {visitor.email}')
            print(f'  - Updated attributes: {visitor.attributes}')

            return visitor

        except Exception as error:
            print(f'✗ Failed to update visitor: {error}')
            raise


def batch_update_visitors(visitor_updates):
    """
    Batch update multiple visitors
    Useful for scheduled jobs or bulk operations
    """

    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        print(f'Updating {len(visitor_updates)} visitors...')

        results = []
        for update in visitor_updates:
            try:
                visitor = visitors_api.visitors_service_update(
                    id=update['id'],
                    visitors_service_update_body=VisitorsServiceUpdateBody(
                        visitor=VisitorInput(data=update['data'])
                    )
                )
                print(f'  ✓ Updated visitor {update["id"]}')
                results.append({'status': 'success', 'visitor': visitor})
            except Exception as error:
                print(f'  ✗ Failed to update visitor {update["id"]}: {error}')
                results.append({'status': 'error', 'error': str(error)})

        succeeded = len([r for r in results if r['status'] == 'success'])
        failed = len([r for r in results if r['status'] == 'error'])

        print(f'\nBatch update complete: {succeeded} succeeded, {failed} failed')

        return results


if __name__ == '__main__':
    try:
        update_visitor()
        print('\n✓ Example completed successfully')
    except Exception as error:
        print(f'\n✗ Example failed: {error}')
        exit(1)
