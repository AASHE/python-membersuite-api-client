# Change Log

## [Unreleased]
### Changed

## [3.3.4] - 2018-02-05
### Breaking Changes

This client can only submit "object" queries to MemberSuite.  "Object"
queries are where the selected element in a query is either "OBJECT()"
or "OBJECTS()".

To make the OBJECT() or OBJECTS() requirement visible, a number of
functions and parameters have been renamed. These might be breaking
changes for your application.

- ConciergeClient.runSQL is renamed ConciergeClient.execute_object_query.

- The `query`` parameter to `execute_object_query` is renamed to `object_query`.

- `utils.submit_msql_query` is renamed to `utils.submit_msql_object_query`.
