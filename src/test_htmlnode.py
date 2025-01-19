import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

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

    def test_leaf_to_html(self):
        node = LeafNode(
            tag = "h1",
            value = "This is a heading",
            props = {
                'role': 'heading',
                'aria-level': '1'
                    })
        expected = '<h1 role="heading" aria-level="1">This is a heading</h1>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_none_tag(self):
        node = LeafNode(
            tag = None,
            value = "This is a heading", 
            props = {
                'role': 'heading',
                'aria-level': '1'
                }
            )
        expected = 'This is a heading'
        self.assertEqual(node.to_html(), expected)

    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
        )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected)

    def test_parent_tag_none(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(
                tag = None,
                children = [
                LeafNode(None, "No tag"),
                LeafNode(None, "What happened")
                ],
            )
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no tag")

    def test_parent_children_none(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(
                tag = "p",
                children = [],
                props = {
                'role': 'heading',
                'aria-level': '1'
                    })
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no children")

    def test_nested_parent_to_html(self):
        node = ParentNode("p", [
            ParentNode("strong", [LeafNode(None, "Nested")])
        ])
        expected = "<p><strong>Nested</strong></p>"
        self.assertEqual(node.to_html(), expected)

    def test_deeply_nested_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "strong",
                    [ParentNode(
                        "em",
                        [LeafNode(None, "Great-grandchild is here")],
                        ),
                    LeafNode(None, "Grandchild is here"),
                    ]
                ),
                LeafNode(None, "Child is here"),
            ]
        )
        expected = '<p><strong><em>Great-grandchild is here</em>Grandchild is here</strong>Child is here</p>'
        self.assertEqual(node.to_html(), expected)
