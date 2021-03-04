import subprocess


def run_curl(request, endpoint):
    """Run a curl request which plays by the rules."""

    command = f"curl {request} http://127.0.0.1:8088/{endpoint}"
    return subprocess.run(command, capture_output=True, text=True)


def post_password(password):
    """POST the password to the hash endpoint."""

    json_object = f"""{{"password":"{password}"}}"""
    return run_curl(
        request=f"""-X POST -H "application/json" -d '{json_object}'""",
        endpoint="hash",
    )


def get_result(index):
    """
    GET the given encoded password hash.
    Correctly, it should be a 1-index integer, but we won't restrict it here
     in order to allow failure testing.
    """

    return run_curl(request='-H "application/json"', endpoint=f"hash/{index}")


def get_first_result():
    """GET the first encoded password hash."""

    return get_result(1)
