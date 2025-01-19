import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        expected = 'TextNode(This is a text node, bold, https://www.boot.dev)'
        self.assertEqual(repr(node), expected)

    def test_text_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html = text_node_to_html_node(node)
        expected = LeafNode(None, "This is a text node")
        self.assertEqual(html, expected)

    def test_bold_to_html_node(self):
        node = TextNode("Bold like coffee", TextType.BOLD)
        html = text_node_to_html_node(node)
        expected = LeafNode("b", "Bold like coffee")
        self.assertEqual(html, expected)

    def test_italic_to_html_node(self):
        node = TextNode("I like it Italic", TextType.ITALIC)
        html = text_node_to_html_node(node)
        expected = LeafNode("i", "I like it Italic")
        self.assertEqual(html, expected)

    def test_code_to_html_node(self):
        node = TextNode("Code is cool", TextType.CODE)
        html = text_node_to_html_node(node)
        expected = LeafNode("code", "Code is cool")
        self.assertEqual(html, expected)
    
    def test_link_to_html_node(self):
        node = TextNode("Click me", TextType.LINK)
        html = text_node_to_html_node(node)
        expected = LeafNode("a", "Click me")
        self.assertEqual(html, expected)

    def text_image_to_html_node(self):
        node = TextNode("An Image", TextType.IMAGE, url="http://example.com/img.png")
        html = text_node_to_html_node(node)
        expected = LeafNode(
            "img",
            "",
            {
                "src": "http://example.com/img.png",
                "alt": "An Image"
            }
        )
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
