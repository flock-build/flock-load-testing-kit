import subprocess


def roost():
    """
    Start FLK Load testing with Locust UI.
    """

    subprocess.run(["locust"], cwd=".")
