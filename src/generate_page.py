import re
import os

from block_markdown import markdown_to_html_node

def extract_title(markdown):
    match = re.search(r"^#\s+([^#].*)$", markdown, flags=re.M)
    if match is None:
        raise ValueError("No h1 heading in md file")
    return match.group(1).strip()
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as file:
        print(template, file=file)


