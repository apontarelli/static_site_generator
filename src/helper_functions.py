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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

