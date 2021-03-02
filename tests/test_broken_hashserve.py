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


@pytest.fixture(scope="class", autouse=True)
def start_server():
    """
    Start the server. Opens the process and does nothing.
    Will autorun for each test class in this module.
    No need to test startup since that's implicit for every other test.
    :return:
    """

    subprocess.Popen(hashserve_exe)


class HashServeOperationTest:
    """
    Test class for regular hashserve operation.
    Test pattern was changed from standard TestFoo to FooTest because that's more
     legible at a glance.
    """

    @staticmethod
    def test_get_base64_password():
        """Test getting the """

        curl = """curl -H "application/json" http://127.0.0.1:8088/hash/1"""
        call = subprocess.run(curl, text=True, check=True)
        ciphertext = "zHkbvZDdwYYiDnwtDdv/FIWvcy1sKCb7qi7Nu8Q8Cd/MqjQeyCI0pWKDGp74A1g=="
        assert call.stdout == ciphertext, (
            "Failed to get the correct base64 password"
            f"\nActual:   {call.stdout}"
            f"\nExpected: {ciphertext}"
        )
