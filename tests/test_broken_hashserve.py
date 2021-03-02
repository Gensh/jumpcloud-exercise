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


def run_curl(request, endpoint):
    """Run a curl request which plays by the rules."""

    command = f"curl {request} http://127.0.0.1:8088/{endpoint}"
    return subprocess.run(command, text=True, check=True)


@pytest.fixture(scope="class", autouse=True)
def start_server():
    """
    Start the server. Opens the process and does nothing.
    Will autorun for each test class in this module.
    No need to test startup since that's implicit for every other test.
    :return:
    """

    subprocess.Popen(hashserve_exe)


class HashServeHashCrudTest:
    """
    Test class for regular hashserve Create/Read/Update/Delete.
    """

    @staticmethod
    def test_get_base64_password():
        """Test getting the """

        result = run_curl(request='-H "application/json"', endpoint="hash/1")
        ciphertext = "zHkbvZDdwYYiDnwtDdv/FIWvcy1sKCb7qi7Nu8Q8Cd/MqjQeyCI0pWKDGp74A1g=="
        assert result.stdout == ciphertext, (
            "Failed to get the correct base64 password"
            f"\nActual:   {result.stdout}"
            f"\nExpected: {ciphertext}"
        )
