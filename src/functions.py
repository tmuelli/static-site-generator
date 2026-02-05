from leafnode import LeafNode
from textnode import TextNode, TextType

def text_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

        case _:
            raise Exception("Invalid text node type.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_nodes.append(node.text_type)
            continue

        # split nodes
        

    return result_nodes