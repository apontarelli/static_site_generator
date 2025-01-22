from utils import copy_src_to_dest
from generate_page import generate_page_recursive

def main():
    copy_src_to_dest("./static", "./public")

    content = "content/" 
    template = "template.html"
    dest = "public/"
    generate_page_recursive(content, template, dest)
main()
