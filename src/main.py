from textnode import TextNode, TextType
from functions import copy_dir, generate_pages_recursive

def main():
    copy_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()