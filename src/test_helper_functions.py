import unittest

from textnode import TextNode, TextType
from helper_functions import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_text_node(self):
        node = [TextNode("This is a simple TextNode `with code` and text", TextType.TEXT)]
        result = split_nodes_delimiter(node, "`", TextType.CODE)
        expected = [
                    TextNode("This is a simple TextNode ", TextType.TEXT),
                    TextNode("with code", TextType.CODE),
                    TextNode(" and text", TextType.TEXT)
                    ]
        self.assertEqual(result, expected)
        
    def test_multiple_text_node(self):
        node1 = [TextNode("This is the first TextNode", TextType.TEXT)]
        node2 = [TextNode("This is the **second** TextNode", TextType.TEXT)]
        node_list = node1 + node2
        result = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected = [
                    TextNode("This is the first TextNode", TextType.TEXT),
                    TextNode("This is the ", TextType.TEXT),
                    TextNode("second", TextType.BOLD),
                    TextNode(" TextNode", TextType.TEXT)
                    ]
        self.assertEqual(result, expected)

    def test_no_delimiter_nodes(self):
        node = [TextNode("This is a simple TextNode", TextType.TEXT)]
        result = split_nodes_delimiter(node, "`", TextType.CODE)
        expected = [TextNode("This is a simple TextNode", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_nontext_node(self):
        node = [TextNode("This is a link TextNode", TextType.LINK)]
        result = split_nodes_delimiter(node, "*", TextType.ITALIC)
        expected = [TextNode("This is a link TextNode", TextType.LINK)]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = [TextNode("This is *very*, **tricky**, *TextNode* business", TextType.TEXT)]
        result = split_nodes_delimiter(node, "*", TextType.ITALIC)
        expected = [TextNode("This is ", TextType.TEXT),
                    TextNode("very", TextType.ITALIC),
                    TextNode(", **tricky**, ", TextType.TEXT),
                    TextNode("TextNode", TextType.ITALIC),
                    TextNode(" business", TextType.TEXT)
                    ]
        pass
        # to implement with nesting logic
        # self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
