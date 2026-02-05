from textnode import TextNode, TextType

def main():
    textnode = TextNode("Bold text", TextType.BOLD, "https://boldtext.com")
    print(textnode)

if __name__ == "__main__":
    main()