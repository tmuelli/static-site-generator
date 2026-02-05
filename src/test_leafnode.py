import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h(self):
        node = LeafNode("h2", "Hello, world!")
        self.assertEqual(node.to_html(), "<h2>Hello, world!</h2>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_fully_printed(self):
        node = LeafNode("div", "Hello, world!", { "href": "https://github.com", "size": "40" })
        self.assertEqual(node.to_html(), "<div href=\"https://github.com\" size=\"40\">Hello, world!</div>")


if __name__ == "__main__":
    unittest.main()