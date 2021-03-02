"""Test module"""

import pathlib
import platform
import subprocess

import pytest

my_os = platform.system()
hashserve_suffix = "win.exe" if my_os == "Windows" else my_os.lower()
base_path = pathlib.Path().absolute()
hashserve_exe = base_path / "broken_hashserve" / f"broken-hashserve_{hashserve_suffix}"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    return subprocess.run(hashserve_exe)


class ATest:
    """
    ATest
    """

    @staticmethod
    def test_a():
        """test_a"""

        raise RuntimeError
