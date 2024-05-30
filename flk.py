import sys

from dotenv import load_dotenv

from utils.fly import fly
from utils.roost import roost

load_dotenv()


def main():
    if sys.argv[1] == "fly" and sys.argv[2] == "llm":
        fly()
    elif sys.argv[1] == "roost":
        roost()
    else:
        print("Usage: flk [fly (cli)|roost (web)]")


if __name__ == "__main__":
    main()
