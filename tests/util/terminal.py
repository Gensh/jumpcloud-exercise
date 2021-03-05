"""
Functions for interacting with terminal subprocesses.
"""

import subprocess


def run_curl(request, endpoint):
    """Run a curl request which plays by the rules."""

    command = f"curl {request} http://127.0.0.1:8088/{endpoint}"
    return subprocess.run(command, capture_output=True, text=True)


def post_password(password):
    """
    POST the password to the hash endpoint.

    $ curl -X POST -H "application/json" -d '{"password":"angrymonkey"}'
     http://127.0.0.1:8088/hash
    > 42
    """

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

    $ curl -H "application/json" http://127.0.0.1:8088/hash/1
    > zHkbvZDdwYYiDnwtDdv/FIWvcy1sKCb7qi7Nu8Q8Cd/MqjQeyCI0pWKDGp74A1g==
    """

    return run_curl(request='-H "application/json"', endpoint=f"hash/{index}")


def get_first_result():
    """GET the first encoded password hash."""

    return get_result(1)


def get_stats():
    """
    GET the stats.

    $ curl http://127.0.0.1:8088/stats
    {"TotalRequests":3,"AverageTime":5004625}
    """

    return run_curl(request="", endpoint="stats")


def shutdown():
    """
    POST the shutdown command.

    $ curl -X POST -d 'shutdown' http://127.0.0.1:8088/hash
    > 200 Empty Response
    """

    return run_curl(request="-X POST -d 'shutdown'", endpoint="hash")
