from language_detecting import run_file
import re

my_file = input("Enter relative path of file: ")
title = input("Enter title: ")
# Remove all but alphanumerics and space
title = re.sub(r"[^\w\s]", '', title)
# Eliminate duplicate whitespaces, replace whitespace with underscore
title = re.sub(r"\s+", '_', title)

if __name__ == "__main__":
    run_file(my_file, title)
