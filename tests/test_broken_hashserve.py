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

import pytest

from .cmd_util import get_first_result, get_result, post_password

# Keep encoded hashes to reduce runtime.
good_passwords = [
    (
        "angrymonkey",
        "MzRkZDBmMDBhYjYyNzlhY2EyNGQ4ZjNmNDFkZTc3MDFlMzMzMWU0NmVmNjQzNzcwNjE4OD"
        "gzOWYwYjQzNzZmZmM1MjE2YmRjY2I1YjBhMDliZWVhOGJiMzZlZjEwZjAyNzdmMzJhOGQw"
        "N2IyMDg4ZDI5NThhMGM2YTdiZTAwZDY=",
    ),
    (
        "abc123",
        "YzcwYjVkZDllYmZiNmY1MWQwOWQ0MTMyYjcxNzBjOWQyMDc1MGE3ODUyZjAwNjgwZjY1Nj"
        "U4ZjAzMTBlODEwMDU2ZTY3NjNjMzRjOWEwMGIwZTk0MDA3NmY1NDQ5NWMxNjlmYzIzMDJj"
        "Y2ViMzEyMDM5MjcxYzQzNDY5NTA3ZGM=",
    ),
    (
        "ａｂｃ１２３",
        "NzQ2YjUxM2Q0MTllZDFhOGRmMGJmMGEwMTY5NDk5OTkwNTFmZjhiMWQ4OTY2ZDNlNTdjYm"
        "Q2NWE5MTFjOGY1ZGRhMWQ0MDJiNzU0ZDkzZGI4OTJlMjcwMTJiOGFlNTYwNmI0YTVlZmE5"
        "OGE0MzliMzU0ZmE4MTRmNjZhYjMwZmQ=",
    ),
    (
        "ᴀʙᴄ123",
        "YWI2NjZmZTE5M2U5NmU4ODAxYjU4MjA5NjQwY2Y2NWExOTY3MTExYmMyZGUxMWY0YTUyYj"
        "c3NjEzMjMzMDc2MWViNTBmZjRlYmE4MjIyMGEzYWVmNDA1MjI5NDkwM2I3MmE2ZGM2Yjg4"
        "YTBiYjMwYTY0MjQwNDE3YzZhMWRjYTE=",
    ),
    (
        "怒っている猿",
        "ZGQyOGVlZmE1MTc5OTgyMTQ5NTYyNmNmZWZlZjY0YTk2MzI2YzIyMGNiYWZjYjEzZWM1MG"
        "FmZGY5NGFkNjcwMTY5NGNhNDE1YzhhZGQ1NzQ0NzEzZWQ0MmE1YzczODAzZTA4M2VmYzAw"
        "M2RkODkwMDA2ODVlMjNiNzUzNDllODA=",
    ),
]


class GetHashTest:
    """
    A `GET` to `/hash` should accept a job identifier.
    It should return the base64 encoded password hash for the corresponding
    `POST` request.
    """

    @staticmethod
    @pytest.mark.parametrize("password, encoded", good_passwords)
    def test_get_good_password(password, encoded):
        """
        When I send a GET request
        I want to get the encoded password
        So I can do my security thing
        :param password: A known good password.
        :param encoded: The base64 encoding of that password.
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
