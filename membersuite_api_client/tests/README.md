# Testing membersuite_api_client

## Configuration

You will need to define the following environment variables:

## General vars:

 - `MS_ACCESS_KEY` - your API key
 - `MS_SECRET_KEY` - your API secret
 - `MS_ASSOCIATION_ID` - your membersuite association id

Until we set up a mechanism for fixtures, you'll need to set up the following:

## Organization vars:

 - `TEST_ORG_NAME` - an existing org's name

## Membership vars:

 - `ORG_ID_WITH_MEMBERSHIPS` - an existing org with a membership or two
 - `ORG_ID_WITHOUT_MEMBERSHIPS` - and w/out

## Security vars:

- `TEST_MS_PORTAL_MEMBER_ID` - member user with portal access
- `TEST_MS_PORTAL_MEMBER_PASS` - password
- `TEST_MS_PORTAL_NONMEMBER_ID` - nonmember with portal access
- `TEST_MS_PORTAL_NONMEMBER_PASS` - password
- `TEST_MS_MEMBER_ORG_NAME` - the name of the member organization
