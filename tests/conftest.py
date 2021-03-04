import pathlib
import platform
import subprocess

import pytest

my_os = platform.system()
hashserve_suffix = "win.exe" if my_os == "Windows" else my_os.lower()
base_path = pathlib.Path().absolute()
hashserve_exe = base_path / "broken_hashserve" / f"broken-hashserve_{hashserve_suffix}"


@pytest.fixture(scope="function", autouse=True)
def start_server():
    """
    Start the server. Opens the process and does nothing.
    Will autorun for each test for the sake of keeping results independent.
     Could be moved back to class-based autorun if index-based collisions could
     be avoided.
    No need to test startup since that's implicit for every other test.
    """

    subprocess.Popen(hashserve_exe)
