from textnode import text_node_to_html_node
from inline_markdown import text_to_text_nodes
from htmlnode import ParentNode
import re

def markdown_to_blocks(markdown):
    split_blocks = markdown.split('\n\n')
    stripped_blocks = list(map(str.strip, split_blocks))
    blocks = list(filter(None, stripped_blocks))
    return blocks

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
    stripped_lines = [line.strip() for line in lines]
    if stripped_lines[0].startswith("1. "):
        i = 1
        for line in stripped_lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for item in blocks:
        children.append(process_block(item))
    html = ParentNode("div", children)
    return html

def process_block(block):
    block_type = block_to_block_type(block)
    match block_type:
        case "heading":
            n = len(re.findall(r'#', block))
            content = re.sub(r"^#{1,6} ", "", block) 
            node = ParentNode(tag = f"h{n}", children = text_to_children(content))
            return node

        case "code":
            content = re.sub(r"^```[\n]?", "", block)
            content = re.sub(r"[\n]?```$", "", content)
            node = ParentNode(
                tag = "pre",
                children = [ParentNode(tag = "code", children = text_to_children(content))])
            return node

        case "quote":
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_line = re.sub(r"^>[ ]?", "", line.strip())
                cleaned_lines.append(cleaned_line)
            content = " ".join(cleaned_lines)
            node = ParentNode(tag = "blockquote", children = text_to_children(content))
            return node
            return node

        case "unordered_list":
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                content = re.sub(r"^[*-] ", "", line.strip())
                child_node = ParentNode(tag = "li", children = text_to_children(content))
                child_nodes.append(child_node)
            node = ParentNode(tag = "ul", children = child_nodes)
            return node

        case "ordered_list":
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                content = re.sub(r"^\d+\. ", "", line.strip())
                child_node = ParentNode(tag = "li", children = text_to_children(content))
                child_nodes.append(child_node)
            node = ParentNode(tag = "ol", children = child_nodes)
            return node

        case "paragraph":
            content = " ".join(line.strip() for line in block.split("\n"))
            node = ParentNode(tag = "p", children = text_to_children(content))
            node = ParentNode(tag = "p", children = text_to_children(content))
            return node
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        nodes.append(html_node)
    return nodes



