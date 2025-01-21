import unittest

from textnode import TextNode, TextType
from helper_functions import (
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes,
        markdown_to_blocks,
        block_to_block_type,
        text_to_children,
        process_block,
        markdown_to_html_node
)
from htmlnode import LeafNode, ParentNode

class TestHelperFunctions(unittest.TestCase):
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

    def test_single_image(self):
        nodes = [TextNode(
            "This is a simple text node with ![this is alt text](https://image.url) with an image",
            TextType.TEXT,
        )]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is a simple text node with ", TextType.TEXT),
            TextNode("this is alt text", TextType.IMAGE, "https://image.url"),
            TextNode(" with an image", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is a simple text node with ![this is alt text](https://image.url) with an image",
                TextType.TEXT),
            TextNode(
                "This is some code", TextType.CODE),
            TextNode(
                "This is another simple text node ![this is alt text](https://image.url) with an image", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is a simple text node with ", TextType.TEXT),
            TextNode("this is alt text", TextType.IMAGE, "https://image.url"),
            TextNode(" with an image", TextType.TEXT),
            TextNode("This is some code", TextType.CODE),
            TextNode("This is another simple text node ", TextType.TEXT),
            TextNode("this is alt text", TextType.IMAGE, "https://image.url"),
            TextNode(" with an image", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_nontext_type(self):
        nodes = [
            TextNode("link here", TextType.LINK, "https://here.dev")
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("link here", TextType.LINK, "https://here.dev")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        nodes = [TextNode(
            "This is a simple text node with ![this is alt text](https://image.url) with an image and ![this is different alt text](https://image-two.url) another image",
            TextType.TEXT,
        )]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is a simple text node with ", TextType.TEXT),
            TextNode("this is alt text", TextType.IMAGE, "https://image.url"),
            TextNode(" with an image and ", TextType.TEXT),
            TextNode("this is different alt text", TextType.IMAGE, "https://image-two.url"),
            TextNode(" another image", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_multiple_complex_nodes(self):
        nodes = [TextNode(
            "This is a simple text node with ![this is alt text](https://image.url) with an image and ![this is different alt text](https://image-two.url) another image",
            TextType.TEXT,
        )]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is a simple text node with ", TextType.TEXT),
            TextNode("this is alt text", TextType.IMAGE, "https://image.url"),
            TextNode(" with an image and ", TextType.TEXT),
            TextNode("this is different alt text", TextType.IMAGE, "https://image-two.url"),
            TextNode(" another image", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_single_link(self):
        nodes = [TextNode(
            "This is a simple text node with [this link](https://link.url)",
            TextType.TEXT,
        )]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a simple text node with ", TextType.TEXT),
            TextNode("this link", TextType.LINK, "https://link.url"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is a simple text node with [this link](https://link.url)",
                TextType.TEXT),
            TextNode(
                "This is some code", TextType.CODE),
            TextNode(
                "This is another simple text node with [another link](https://link-two.url)", TextType.TEXT),
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a simple text node with ", TextType.TEXT),
            TextNode("this link", TextType.LINK, "https://link.url"),
            TextNode("This is some code", TextType.CODE),
            TextNode("This is another simple text node with ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://link-two.url"),
        ]
        self.assertEqual(result, expected)

    def test_nontext_type(self):
        nodes = [
            TextNode("link here", TextType.LINK, "https://here.dev")
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("link here", TextType.LINK, "https://here.dev")
        ]
        self.assertEqual(result, expected)      

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

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_mixed_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://*boot*.dev)"
        result = text_to_textnodes(text)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://*boot*.dev"),
        ]
        self.assertEqual(result, expected)

    def test_mismatched_tags(self):
        text = "This is **text with an *italic** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text with an *italic", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_minimal_text(self):
        text = "[link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [TextNode("link", TextType.LINK, "https://example.com")]
        self.assertEqual(result, expected)

    def test_raw_text(self):
        text = "nothing special at all. the most boring text in the world. never ending text that goes on and on and on and on"
        result = text_to_textnodes(text)
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_broken_markdown(self):
        text = "This is **text** with an *italic* word and a code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link]https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a code block` and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a [link]https://boot.dev)", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

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
