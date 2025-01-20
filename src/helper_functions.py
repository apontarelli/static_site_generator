from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        while True:
            parts = remaining_text.split(delimiter, 2)
            if len(parts) < 3:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                break
            before, snippet, after = parts
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(snippet, text_type))
            remaining_text = after
    return new_nodes 

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        tuples = extract_markdown_images(remaining_text)
        if len(tuples) == 0:
            new_nodes.append(old_node)
            continue
        for tuple in tuples:
            sections = remaining_text.split(f"![{tuple[0]}]({tuple[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
            remaining_text = sections[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        tuples = extract_markdown_links(remaining_text)
        if len(tuples) == 0:
            new_nodes.append(old_node)
            continue
        for tuple in tuples:
            sections = remaining_text.split(f"[{tuple[0]}]({tuple[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
            remaining_text = sections[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def markdown_to_blocks(markdown):
    split_blocks = markdown.strip().split('\n\n')
    stripped_blocks = list(map(str.strip, split_blocks))
    blocks = list(filter(None, stripped_blocks))
    return blocks

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([text_node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def block_to_block_type(markdown):
    if re.match(r"^#{1,6}", markdown):
        return "heading"
    if re.match(r"^```(.*?)```$", markdown, re.DOTALL):
        return "code"
    if re.match(r"^>", markdown, re.MULTILINE):
        return "quote"
    if re.match(r"^[*-] ", markdown, re.MULTILINE):
        return "unordered_list"
    lines = markdown.split("\n")
    expected_number = 1
    for line in lines: 
        if re.match(rf"^{expected_number}\. ", line):
            expected_number += 1
            continue
        else:
            break
    else:
        return "ordered_list"
    return "paragraph"  

