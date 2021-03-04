import pathlib
import platform
import subprocess

import pytest


def _make_hashserve_exe_path():
    """Get the full path to the executable for the running OS."""

    my_os = platform.system()
    hashserve_suffix = "win.exe" if my_os == "Windows" else my_os.lower()
    base_path = pathlib.Path().absolute()
    return base_path / "broken_hashserve" / f"broken-hashserve_{hashserve_suffix}"


@pytest.fixture(scope="function", autouse=True)
def start_server(request):
    """
    Start the server. Opens the process and does nothing.
    Will autorun for each test for the sake of keeping results independent.
     Could be moved back to class-based autorun if index-based collisions could
     be avoided.
    No need to test startup since that's implicit for every other test.
    """

    # Skip if test marked no_server.
    if "no_server" in request.keywords:
        return

    subprocess.Popen(hashserve_exe)


hashserve_exe = _make_hashserve_exe_path()
