from retrying import retry


class ChunkQueryMixin():
    """
    A mixin for API client service classes that makes it easy to consistently
    request multiple queries from a MemberSuite endpoint.

    Membersuite will often time out on big queries, so this allows us to
    break it up into smaller requests.

    Design assumptions:
        - The service defines an `result_to_models` method to "transform"
        the objects returned by the endpoint
    """

    def get_long_query(
            self, base_query, retry_attempts=2, limit_to=200, max_calls=None):
        """
        Takes a base query for all objects and recursively requests them

        @base_query - the base query to be executed
        @retry_attempts - the number of times to retry a query when it fails
        @limit_to - how many rows to query for in each chunk
        @max_recursion_depth - None is infinite
        """

        @retry(stop_max_attempt_number=retry_attempts)
        def run_query(base_query, start_record, limit_to):
            # inline method to take advantage of retry
            result = self.client.runSQL(
                query=base_query,
                start_record=start_record,
                limit_to=limit_to,
            )
            return self.result_to_models(result)

        record_index = 0
        result = run_query(base_query, record_index, limit_to)
        all_objects = result
        call_count = 1
        """
        continue to run queries as long as we
            - don't exceed the call call_count
            - don't see results that are less than the limited length (the end)
        """
        while (
                call_count != max_calls and
                len(result) >= limit_to):

            record_index += len(result)  # should be `limit_to`
            all_objects += run_query(base_query, record_index, limit_to)
            call_count += 1

        return all_objects
