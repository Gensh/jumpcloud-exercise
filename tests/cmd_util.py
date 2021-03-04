import subprocess


def run_curl(request, endpoint):
    """Run a curl request which plays by the rules."""

    command = f"curl {request} http://127.0.0.1:8088/{endpoint}"
    return subprocess.run(command, capture_output=True, text=True)
