from language_detecting import run_file
import re

my_file = input("Enter relative path of file: ")
title = input("Enter title: ")
title = re.sub(r"[^\w\s]", '', title)
title = re.sub(r"\s+", '_', title)

if __name__ == "__main__":
    run_file(my_file, title)
