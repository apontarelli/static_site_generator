import unittest

from textnode import TextNode, TextType
from helper_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This ![amazing image](https://image.url) is an amazing image"
        result = extract_markdown_images(text)
        expected = [("amazing image", "https://image.url")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = "This is first ![first image](https://first_image.url) and second ![second image](https://second_image.url) image in the string."
        result = extract_markdown_images(text)
        expected = [
                ("first image", "https://first_image.url"),
                ("second image", "https://second_image.url")
                ]
        self.assertEqual(result, expected)

    def test_image_with_exclamation(self):
        text = "This ![amazing image](https://image.url) is an amazing image!"
        result = extract_markdown_images(text)
        expected = [("amazing image", "https://image.url")]
        self.assertEqual(result, expected)

    def test_image_with_no_alt_text(self):
        text = "This ![](https://image.url) is a boring image!"
        result = extract_markdown_images(text)
        expected = [("", "https://image.url")]
        self.assertEqual(result, expected)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_links(self):
        text = "This [amazing link](https://link.url) is an amazing image"
        result = extract_markdown_links(text)
        expected = [("amazing link", "https://link.url")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = "This is first [first link](https://first_link.url) and second [second link](https://second_link.url) link in the string."
        result = extract_markdown_links(text)
        expected = [
                ("first link", "https://first_link.url"),
                ("second link", "https://second_link.url")
                ]
        self.assertEqual(result, expected)

    def test_link_with_parenthesis(self):
        text = "This [amazing link](https://link.url) is an amazing (but simple) link!"
        result = extract_markdown_links(text)
        expected = [("amazing link", "https://link.url")]
        self.assertEqual(result, expected)

    def test_link_with_brackets(self):
        text = "This [another link](https://link.url) is a simple image [with some brackets]!"
        result = extract_markdown_links(text)
        expected = [("another link", "https://link.url")]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
