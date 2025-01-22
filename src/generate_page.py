import re
import os
from pathlib import Path

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

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    path = Path(dir_path_content)
    for entry in path.iterdir():
        if entry.is_file() and entry.suffix == '.md':
            rel_path = entry.relative_to(path)
            dest_path = Path(dest_dir_path) / rel_path
            generate_page(str(entry), template_path, str(dest_path.with_suffix('.html')))
        elif entry.is_dir():
            new_dest_dir = Path(dest_dir_path) / entry.name
            generate_page_recursive(str(entry), template_path, str(new_dest_dir))
