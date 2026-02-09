import unittest

from functions import (
    text_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_links,
    split_nodes_images,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title
)
from textnode import TextNode, TextType
from blocktype import BlockType

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

    def test_split_code_node(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.PLAIN))

    def test_split_multi_code_node(self):
        node = TextNode("This is text with a `code block` word. And another `one` here.", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word. And another ", TextType.PLAIN))
        self.assertEqual(new_nodes[3], TextNode("one", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode(" here.", TextType.PLAIN))

    def test_split_multi_code_nodes(self):
        node = TextNode("This is text with a `code block` word. And another `one` here.", TextType.PLAIN)
        node2 = TextNode("And here is even a `second` node itself!", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 8)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word. And another ", TextType.PLAIN))
        self.assertEqual(new_nodes[3], TextNode("one", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode(" here.", TextType.PLAIN))
        self.assertEqual(new_nodes[5], TextNode("And here is even a ", TextType.PLAIN))
        self.assertEqual(new_nodes[6], TextNode("second", TextType.CODE))
        self.assertEqual(new_nodes[7], TextNode(" node itself!", TextType.PLAIN))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link to google](https://google.com)"
        )
        self.assertListEqual([("link to google", "https://google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link1](https://i.imgur.com/zjjcJKZ.png) and another [link2](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        md = "### Heading at level 3"
        self.assertEqual(
            block_to_block_type(md),
            BlockType.HEADING
        )
        md_fail = "##Invalid Heading, just paragraph."
        b_type = block_to_block_type(md_fail)
        self.assertNotEqual(b_type, BlockType.HEADING)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md = """```
Code block
```"""
        self.assertEqual(
            block_to_block_type(md),
            BlockType.CODE
        )

    def test_block_to_block_type_ulist(self):
        md ="""- list entry 1
- list entry 2
- list entry 3"""

        self.assertEqual(
            block_to_block_type(md),
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_olist(self):
        md = """1. list entry 1
2. list entry 2
3. list entry 3"""

        self.assertEqual(
            block_to_block_type(md),
            BlockType.ORDERED_LIST
        )

        md_fail = """2. list entry 1
1. list entry 2
3. list entry 3"""
        self.assertNotEqual(
            block_to_block_type(md_fail),
            BlockType.ORDERED_LIST
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
# Heading Title at Level 1

Other stuff here and there.
Paragraphs bla bla bla.
"""
        title = extract_title(md)
        self.assertEqual(title, "Heading Title at Level 1")