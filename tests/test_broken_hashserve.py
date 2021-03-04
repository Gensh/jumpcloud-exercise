"""
Module containing all tests for the broken hashserve executable.
"""

import pytest

from .cmd_util import run_curl

good_passwords = [
    ("abc123", "YWJjMTIz"),
]


class HashServeGetTest:
    """
    Tests for GET requests.
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

        # Put the password in.
        json_object = f"""{{"password":"{password}"}}"""
        run_curl(
            request=f"""-X POST -H "application/json" -d '{json_object}'""",
            endpoint="hash",
        )

        # Get the encoded version out.
        result = run_curl(request='-H "application/json"', endpoint="hash/1")
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

        result = run_curl(request='-H "application/json"', endpoint="hash/1")
        assert result.returncode != 200, "Received code 200 when in error state"
        assert (
            result.returncode != 0
        ), "Did not receive a return code when in error state"
        assert result.stdout is None, (
            "Found a password when expecting an empty database"
            f"\nActual:   {result.stdout}"
        )
