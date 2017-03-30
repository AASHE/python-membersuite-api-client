# Testing membersuite_api_client

## Configuration

You will need to define the following environment variables:

## General vars:

 - `MS_ACCESS_KEY` - your API key
 - `MS_SECRET_KEY` - your API secret
 - `MS_ASSOCIATION_ID` - your membersuite association id

Until we set up a mechanism for fixtures, you'll need to set up the following:

## Organization vars:

 - `TEST_ORG_ID` - an existing org

## Membership vars:

 - `ORG_ID_WITH_MEMBERSHIPS` - an existing org with a membership or two
 - `ORG_ID_WITHOUT_MEMBERSHIPS` - and w/out

## Security vars:

 - `TEST_MS_PORTAL_USER_ID` - a user with portal access
 - `TEST_MS_PORTAL_USER_PASS` - that user's password
