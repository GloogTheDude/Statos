from textnode import TextNode,TextType
import os
import shutil
from dir_manip import *
from gencontent import *

public = "./public"
static = "./static"
print(get_list_dir_from(public))
clear_dir(public)
print(get_list_dir_from(public))
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


"""generate_page(from_path="content/index.md", template_path="template.html",dest_path ="public/index.html")
for k in blog.keys():
    generate_page(blog[k][0],template_path, blog[k][1])"""

generate_pages_recursive("./content", template_path, public)
