import sys

from utils.fly import fly
from utils.roost import roost


def main():
    if sys.argv[1] == "fly" and sys.argv[2] == "llm":
        fly()
    elif sys.argv[1] == "roost":
        roost()
    else:
        print("Usage: flk [fly (cli)|roost (web)]")


if __name__ == "__main__":
    main()
