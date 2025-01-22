import re

def extract_title(markdown):
    match = re.search(r"^#\s+([^#].*)$", markdown, flags=re.M)
    if match is None:
        raise ValueError("No h1 heading in md file")
    return match.group(1).strip()
    
def generate_page(from_path, template_path, dest_path):
    pass

