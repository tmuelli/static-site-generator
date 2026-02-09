import sys

from textnode import TextNode, TextType
from functions import copy_dir, generate_pages_recursive

def main():
    basepath = "/"
    if (len(sys.argv) > 1) and sys.argv[1] is not None and sys.argv[1] != "":
        basepath = sys.argv[1]

    copy_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()