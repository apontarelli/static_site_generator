import unittest

from block_markdown import (
        markdown_to_blocks,
        block_to_block_type,
        text_to_children,
        process_block,
        markdown_to_html_node
)
from htmlnode import LeafNode, ParentNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n        * This is a list item\n        * This is another list item"
            ]
        self.assertEqual(result, expected)

    def test_many_newlines_to_blocks(self):
        text = """# This is a heading



        This is a paragraph of text. It has some **bold** and *italic* words inside of it.



        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n        * This is a list item\n        * This is another list item"
            ]
        self.assertEqual(result, expected)

    def test_heading_to_block_type(self):
        text = "### This is a h3"
        result = block_to_block_type(text)
        expected = "heading"
        self.assertEqual(result, expected)

    def test_code_to_block_type(self):
        text = "```This is some code\nthis is another line of code \nthe most code```"
        result = block_to_block_type(text)
        expected = "code"
        self.assertEqual(result, expected)

    def test_quote_to_block_type(self):
        text = ">This is a quote\n>The quote continues on\n>will this person ever stop talking"
        result = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(result, expected)

    def test_unordered_to_block_type(self):
        text = "- This is an unordered list\n* another list item with an *\n- last item i promise"
        result = block_to_block_type(text)
        expected = "unordered_list"
        self.assertEqual(result, expected)

    def test_ordered_to_block_type(self):
        text = "1. This is the first item\n2. This is the second item\n3. This is the last item"
        result = block_to_block_type(text)
        expected = "ordered_list"
        self.assertEqual(result, expected)

    def test_paragraph_to_block_type(self):
        text = "1. This is the first item\n* This is the second item\n3. This is the last item"
        result = block_to_block_type(text)
        expected = "paragraph"
        self.assertEqual(result, expected)

    def test_text_to_children(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_children(text)
        expected = [
            LeafNode(None, "This is "),
            LeafNode("b", "text"),
            LeafNode(None, " with an "),
            LeafNode("i", "italic"),
            LeafNode(None, " word and a "),
            LeafNode("code", "code block"),
            LeafNode(None, " and an "),
            LeafNode("img", "", {
                    "src": "https://i.imgur.com/fJRm4Vk.jpeg",
                    "alt": "obi wan image"}),
            LeafNode(None, " and a "),
            LeafNode("a", "link", {"href":"https://boot.dev"}),
        ]
        self.assertEqual(result, expected)

    def test_process_heading(self):
        text = "# This is a heading"
        result = process_block(text)
        expected = ParentNode(
            "h1",
            [LeafNode(None, "This is a heading")])
        self.assertEqual(result, expected)

    def test_process_code(self):
        text = "```This is some code\nthis is another line of code \nthe most code```"
        result = process_block(text)
        expected = ParentNode(
            "pre",
            [ParentNode(tag = "code", children = [
                LeafNode(None, "This is some code\nthis is another line of code \nthe most code")
                ])])
        self.assertEqual(result, expected)

    def test_process_quote(self):
        text = ">This is a quote\n>The quote continues on\n>will this person ever stop talking"
        result = process_block(text)
        expected = ParentNode(
            tag = "blockquote",
            children = [LeafNode(None, "This is a quote The quote continues on will this person ever stop talking")])
        self.assertEqual(result, expected)

    def test_process_unordered_list(self):
        text = "- This is an unordered list\n* another list item with an *\n- last item i promise"
        result = process_block(text)
        expected = ParentNode(
            tag = "ul",
            children = [
                ParentNode("li", children = [LeafNode(None, "This is an unordered list")]),
                ParentNode("li", children = [LeafNode(None, "another list item with an *")]),
                ParentNode("li", children = [LeafNode(None, "last item i promise")])])
        self.assertEqual(result, expected)

    def test_process_ordered_list(self):
        text = "1. This is the first item\n2. This is the second item\n3. This is the last item"
        result = process_block(text)
        expected = ParentNode(
            tag = "ol",
            children = [
                ParentNode("li", children = [LeafNode(None, "This is the first item")]),
                ParentNode("li", children = [LeafNode(None, "This is the second item")]),
                ParentNode("li", children = [LeafNode(None, "This is the last item")])])
        self.assertEqual(result, expected)

    def test_process_paragraph(self):
        text = "1. This is the first item\n* This is the second item\n3. This is the last item"
        result = process_block(text)
        expected = ParentNode(
            tag = "p",
            children = [LeafNode(None, "1. This is the first item * This is the second item 3. This is the last item")])
        self.assertEqual(result, expected)

    def test_paragraph(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with *italic* text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
        - This is a list
        - with items
        - and *more* items

        1. This is an `ordered` list
        2. with items
        3. and more items

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
        # this is an h1

        this is paragraph text

        ## this is an h2
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
        > This is a
        > blockquote block

        this is paragraph text

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
if __name__ == "__main__":
    unittest.main()
