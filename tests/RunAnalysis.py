import sys

from language_detecting import run_file

if __name__ == "__main__":
    run_file(sys.stdin, sys.stdin, sys.stdout)
