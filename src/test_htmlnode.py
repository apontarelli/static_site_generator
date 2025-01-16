import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html(self):
        node = HtmlNode(
            tag = "h1",
            value = "This is a heading", 
            children = [HtmlNode(
                tag = "text", 
                value = "This is some text"
            )])
        self.assertRaises(NotImplementedError, node.to_html) 

    def test_props_to_html(self):
        node = HtmlNode(
            tag = "h1",
            value = "This is a heading", 
            children = [HtmlNode(
                tag = "text", 
                value = "This is some text")],
            props = {
                'role': 'heading',
                'aria-level': '1'
                }
            )
        expected = ' role="heading" aria-level="1"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HtmlNode(
            tag = "h1",
            value = "This is a heading", 
            children = [HtmlNode(
                tag = "text", 
                value = "This is some text"
            )])
        expected = 'HtmlNode(h1, This is a heading, [HtmlNode(text, This is some text, None, None)], None)'
        self.assertEqual(repr(node), expected)
