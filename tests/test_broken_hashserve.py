"""
Module containing all tests for the broken hashserve executable.
"""

import pathlib
import platform
import subprocess

import pytest

my_os = platform.system()
hashserve_suffix = "win.exe" if my_os == "Windows" else my_os.lower()
base_path = pathlib.Path().absolute()
hashserve_exe = base_path / "broken_hashserve" / f"broken-hashserve_{hashserve_suffix}"


good_passwords = [
    ("abc123", "YWJjMTIz"),
]


def run_curl(request, endpoint):
    """Run a curl request which plays by the rules."""

    command = f"curl {request} http://127.0.0.1:8088/{endpoint}"
    return subprocess.run(command, text=True)


@pytest.fixture(scope="function", autouse=True)
def start_server():
    """
    Start the server. Opens the process and does nothing.
    Will autorun for each test for the sake of keeping results independent.
     Could be moved back to class-based if index-based collisions could be avoided.
    No need to test startup since that's implicit for every other test.
    :return:
    """

    subprocess.Popen(hashserve_exe)


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
