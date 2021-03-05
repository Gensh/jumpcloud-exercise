"""
- When launched, the application should wait for http connections.
- It should answer on the `PORT` specified in the `PORT` environment variable.
- It should support three endpoints:
    - A `POST` to `/hash` should accept a password.
      It should return a job identifier immediately.
      It should then wait 5 seconds and compute the password hash.
      The hashing algorithm should be SHA512.
    - A `GET` to `/hash` should accept a job identifier.
      It should return the base64 encoded password hash for the corresponding
      `POST` request.
    - A `GET` to `/stats` should accept no data.
      It should return a JSON data structure for the total hash requests since
      the server started and the average time of a hash request in milliseconds.
- The software should be able to process multiple connections simultaneously.
- The software should support a graceful shutdown request. Meaning, it should
  allow any in-flight password hashing to complete, reject any new requests,
  respond with a `200` and shutdown.
- No additional password requests should be allowed when shutdown is pending.
"""

import json
import subprocess

import pytest

from tests.util.data import good_passwords
from tests.util.terminal import get_first_result, get_result, get_stats, post_password

"""
Requirements implicitly tested:
- When launched, the application should wait for http connections.
- It should answer on the `PORT` specified in the `PORT` environment variable.
"""


class HashTest:
    """
    A `POST` to `/hash` should accept a password.
    It should return a job identifier immediately.
    It should then wait 5 seconds and compute the password hash.
    The hashing algorithm should be SHA512.

    A `GET` to `/hash` should accept a job identifier.
    It should return the base64 encoded password hash for the corresponding
     `POST` request.
    """

    @staticmethod
    @pytest.mark.parametrize("password, encoded", good_passwords)
    def test_post_return_immediately(password, encoded):
        """
        When I send a POST request
        I want to get the job ID immediately
        So I can go back and check the result when it's ready
        :param password: A known good password.
        :param encoded: The base64 encoded password hash.
        """

        def post_password_nowait():
            """
            POST the password to the hash endpoint but don't wait for it to return.
            """

            json_object = f"""{{"password":"{password}"}}"""
            request = f"""-X POST -H "application/json" -d '{json_object}'"""
            command = f"curl {request} http://127.0.0.1:8088/hash"
            return subprocess.Popen(
                command, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
            )

        post_return = post_password_nowait()
        assert post_return.stdout, "Did not return immediately"
        assert str.isdigit(f"{post_return.stdout}"), (
            "Did not return a valid job ID"
            f"\nActual:   {post_return.stdout}"
            f"\nExpected: 1"
        )

    @staticmethod
    @pytest.mark.parametrize("password, encoded", good_passwords)
    def test_get_good_password(password, encoded):
        """
        When I send a GET request
        I want to get the encoded password
        So I can do my security thing
        :param password: A known good password.
        :param encoded: The base64 encoded password hash.
        """

        post_password(password)
        result = get_first_result()
        assert result.returncode == 200, (
            "Received a return code other than 200" f"\nActual:   {result.returncode}"
        )
        assert result.stdout == encoded, (
            "Failed to get the correct base64 password"
            f"\nActual:   {result.stdout}"
            f"\nExpected: {encoded}"
        )

    @staticmethod
    def test_fail_if_empty():
        """
        When I send a GET request to an empty database
        I want to receive an error code
        So I can readily recognize the issue
        """

        result = get_first_result()
        assert result.returncode != 200, "Received code 200 when in error state"
        assert (
            result.returncode != 0
        ), "Did not receive a return code when in error state"
        assert result.stdout is None, (
            "Found a password when expecting an empty database"
            f"\nActual:   {result.stdout}"
        )

    @staticmethod
    def test_fail_if_bad_job_id():
        """
        When I send a GET request with a bad job ID
        I want to receive an error code
        So I can readily recognize the issue
        """

        post_password("foo")
        result = get_result(2)
        assert result.returncode != 200, "Received code 200 when in error state"
        assert (
            result.returncode != 0
        ), "Did not receive a return code when in error state"
        assert result.stdout is None, (
            "Found a password given a bad job ID" f"\nActual:   {result.stdout}"
        )

    @staticmethod
    def test_fail_if_string_job_id():
        """
        When I send a GET request with a string job ID instead of an integer
        I want to receive an error code
        So I can readily recognize the issue

        Explicitly check string in case storage is ever reimplemented as a map.
        """

        post_password("foo")
        result = get_result("foo")
        assert result.returncode != 200, "Received code 200 when in error state"
        assert (
            result.returncode != 0
        ), "Did not receive a return code when in error state"
        assert result.stdout is None, (
            "Found a password given a string key" f"\nActual:   {result.stdout}"
        )


class StatsTest:
    """
    A `GET` to `/stats` should accept no data.
    It should return a JSON data structure for the total hash requests since
     the server started and the average time of a hash request in milliseconds.
    """

    @staticmethod
    def test_get_stats_updates():
        """
        When I send a GET request
        I want to see the stats have updated since my last request
        So I can trust the integrity of my data
        """

        def update_stats():
            raw_stats = get_stats()
            assert raw_stats.stdout, "Failed to get stats"

            decoded_stats = json.loads(raw_stats.stdout)

            requests = decoded_stats.get("TotalRequests")
            time = decoded_stats.get("AverageTime")

            assert requests, "Stats don't include total requests"
            assert time, "Stats don't include average time"

            return requests, time

        last_requests, last_time = update_stats()

        time_updates = False

        my_passwords = ["foo", "bar"]
        for index in range(1, len(my_passwords)):
            post_password(my_passwords[index])
            current_requests, current_time = update_stats()
            assert (
                current_requests > last_requests
            ), "Didn't update total requests after POST"
            time_updates = True if time_updates else current_time != last_time
            last_requests = current_requests
            last_time = current_time

            get_result(index)
            current_requests, current_time = update_stats()
            assert (
                current_requests > last_requests
            ), "Didn't update total requests after GET"
            time_updates = True if time_updates else current_time != last_time
            last_requests = current_requests
            last_time = current_time

        assert time_updates, "Never updated average time"


class MultipleAccessTest:
    """
    The software should be able to process multiple connections simultaneously.
    """


class ShutdownTest:
    """
    The software should support a graceful shutdown request. Meaning, it should
     allow any in-flight password hashing to complete, reject any new requests,
     respond with a `200` and shutdown.
    No additional password requests should be allowed when shutdown is pending.
    """
