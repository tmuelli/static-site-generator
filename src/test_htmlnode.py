import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_tag(self):
        node = HTMLNode("p", "test", ["div"], { "href": "https://github.com", "size": "50" })
        node2 = HTMLNode("p", "test123", ["div"], { "href": "https://github.com", "size": "40" })
        self.assertTrue(node.tag == node2.tag)

    def test_eq_value(self):
        node = HTMLNode("h", "test", [], { "href": "https://github.com" })
        node2 = HTMLNode("p", "test", [], { "href": "https://github.com" })
        self.assertTrue(node.value == node2.value)

    def test_children_empty(self):
        node = HTMLNode("p", "test", [], { "href": "https://github.com" })
        self.assertTrue(len(node.children) == 0)

    def test_has_children(self):
        node = HTMLNode("p", "test", ["div"], { "href": "https://github.com" })
        self.assertTrue(len(node.children) != 0)


if __name__ == "__main__":
    unittest.main()