import subprocess
import sys


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "fly":
            subprocess.run(
                ["locust", "--headless", "-u", "100", "--run-time", "1h30m"], cwd="."
            )
        elif sys.argv[1] == "roost":
            subprocess.run(["locust"], cwd=".")
        else:
            print("Usage: flk [fly (headless)|roost (web)]")
    else:
        print("Usage: flk [fly (headless)|roost (web)]")


if __name__ == "__main__":
    main()
