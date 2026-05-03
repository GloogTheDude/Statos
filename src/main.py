from textnode import TextNode,TextType
import os
import sys
import shutil
from dir_manip import *
from gencontent import *

public = "./public"
static = "./static"

clear_dir(public)
copy_dir(static,public)
from_path="content/index.md"
template_path="template.html"
dest_path ="public/index.html"
blog={
    "glorfindel": ("content/blog/glorfindel/index.md","public/blog/glorfindel/index.html"),
    "majesty": ("content/blog/majesty/index.md","public/blog/majesty/index.html"),
    "tom" : ("content/blog/tom/index.md","public/blog/tom/index.html"),
    "contact" : ("content/contact/index.md","public/contact/index.html")
}

base_path ="/"
if len(sys.argv) >1:
    base_path = sys.argv[1]

generate_pages_recursive(f"./content", template_path, f"./docs",base_path)
