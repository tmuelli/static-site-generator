import unittest

from functions import text_to_html_node
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "google.com")
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertTrue("href" in html_node.props)
        self.assertEqual(html_node.props["href"], "google.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "picture.com")
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertTrue(html_node.value is None or html_node.value == "")
        self.assertTrue("src" in html_node.props)
        self.assertTrue("alt" in html_node.props)
        self.assertEqual(html_node.props["src"], "picture.com")
        self.assertEqual(html_node.props["alt"], "This is an image node")