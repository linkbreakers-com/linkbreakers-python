"""
Identify Visitor Example

This example demonstrates how to identify a visitor using their LBID
(Linkbreakers ID - a base64 encoded event ID from click/scan tracking).

The identify endpoint will:
- Find an existing visitor by LBID OR
- Create a new visitor profile if one doesn't exist
- Merge the provided system fields and custom attributes

Use Cases:
- User signs up or logs in -> identify them with their email
- User fills out a form -> capture their contact info
- User makes a purchase -> record their plan/subscription
- Enrich visitor data from your CRM or database
"""

import os
from linkbreakers import (
    Configuration,
    ApiClient,
    VisitorsApi,
    IdentifyRequest,
    VisitorInput
)


def identify_visitor():
    """Identify a visitor using their LBID"""

    # Configuration using environment variable
    # Set LINKBREAKERS_API_KEY in your .env file
    configuration = Configuration(
        access_token=os.getenv('LINKBREAKERS_API_KEY', 'your-api-key-here'),
        host='https://api.linkbreakers.com'
    )

    with ApiClient(configuration) as api_client:
        visitors_api = VisitorsApi(api_client)

        # Example LBID (base64 encoded event ID)
        #
        # In production, the LBID comes from:
        # 1. Tracking cookie set by Linkbreakers JS snippet
        # 2. Query parameter ?lbid=... when visitor clicks a link
        # 3. Webhook payload when visitor interacts with your link
        #
        # Format: base64(workspace_id + event_id + timestamp)
        # This example uses a realistic-looking fake LBID
        example_lbid = 'ZXhhbXBsZS1saW5rYnJlYWtlcnMtaWQtMTIzNDU2Nzg5MA=='

        try:
            response = visitors_api.visitors_service_identify(
                identify_request=IdentifyRequest(
                    lbid=example_lbid,

                    visitor=VisitorInput(
                        data={
                            # System fields (prefixed with "$")
                            # These map to standard visitor properties in Linkbreakers
                            '$email': 'john.doe@example.com',
                            '$phone': '+14155551234',
                            '$firstName': 'John',
                            '$lastName': 'Doe',

                            # Custom attributes (no "$" prefix)
                            # Store any additional data you need for segmentation,
                            # personalization, or analytics
                            'company': 'Acme Corporation',
                            'jobTitle': 'Product Manager',
                            'plan': 'premium',
                            'signupDate': '2024-01-15',
                            'industry': 'SaaS',
                            'employeeCount': 50,
                            'source': 'landing-page',
                            'referralCode': 'FRIEND2024'
                        }
                    ),

                    # setOnce: Controls merge behavior
                    #
                    # False (default): Always update fields (overwrites existing values)
                    # True: Only set fields that are currently empty (preserves existing data)
                    #
                    # Use set_once=True for immutable data like signup source or referral code
                    set_once=False
                )
            )

            # Response indicates if a new profile was created or existing one was updated
            print('✓ Visitor identified successfully')
            print(f'  - Created new profile: {response.created}')
            print(f'  - Visitor ID: {response.visitor.id}')
            print(f'  - Email: {response.visitor.email}')
            print(f'  - Phone: {response.visitor.phone}')
            print(f'  - Name: {response.visitor.first_name} {response.visitor.last_name}')
            print(f'  - Custom attributes: {response.visitor.attributes}')

            return response.visitor

        except Exception as error:
            print(f'✗ Failed to identify visitor: {error}')
            raise


if __name__ == '__main__':
    try:
        identify_visitor()
        print('\n✓ Example completed successfully')
    except Exception as error:
        print(f'\n✗ Example failed: {error}')
        exit(1)
