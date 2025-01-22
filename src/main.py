from utils import copy_src_to_dest
from generate_page import generate_page

def main():
    copy_src_to_dest("./static", "./public")

    content = "content/index.md" 
    template = "template.html"
    dest = "public/index.html"
    generate_page(content, template, dest)
main()
