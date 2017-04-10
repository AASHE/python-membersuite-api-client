# Testing membersuite_api_client

## Configuration

You will need to define the following environment variables:

## General vars:

 - `MS_ACCESS_KEY` - your API key
 - `MS_SECRET_KEY` - your API secret
 - `MS_ASSOCIATION_ID` - your membersuite association id

Until we set up a mechanism for fixtures, you'll need to set up the following:

## Membership vars:

 - `ORG_ID_WITH_MEMBERSHIPS` - an existing org with a membership or two
 - `ORG_ID_WITHOUT_MEMBERSHIPS` - and w/out

## Security vars:

- `TEST_MS_MEMBER_ORG_NAME` - the name of the member organization
- `TEST_MS_MEMBER_PORTAL_USER_ID` - member user with portal access
- `TEST_MS_MEMBER_PORTAL_USER_PASSWORD` - password
- `TEST_MS_NONMEMBER_PORTAL_USER_ID` - nonmember with portal access
- `TEST_MS_NONMENGER_PORTAL_USER_PASSWORD` - password

## Subscription vars:

 - `TEST_MS_SUBSCRIBER_ORG_ID` - org that has subscriptions
 - `TEST_MS_PUBLICATION_ID` - a publication for the subscription above
