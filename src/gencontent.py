import os
from markdown_block import *
from dir_manip import *

def extract_title(text):
    lines = text.split("\n")
    for l in lines: 
        if l.startswith("# "):
            title = l[2:]
            return title.strip()
    raise Exception("provided text ain't starting with #")


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path.replace("./",base_path)} using {template_path}.")

    if not os.path.exists(from_path):
        raise ValueError(f"{from_path} does'nt exist")
    if not os.path.isfile(from_path):
        raise ValueError(f"{from_path} is no file")
    if not os.path.exists(template_path):
        raise ValueError(f"{template_path} does'nt exist")
    if not os.path.isfile(template_path):
        raise ValueError(f"{template_path} is no file")
    dest_path_parent = os.path.dirname(dest_path)
    os.makedirs(dest_path_parent,exist_ok=True)
    
    markdown =""
    template=""
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path,"r") as f2:
        template =f2.read()
        
    title = extract_title(markdown)
    html_blocks = markdown_to_html_node(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_blocks.to_html())
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    with open(dest_path, "w") as f3:
        f3.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,base_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}.")
    if not os.path.exists(dir_path_content):
        raise ValueError(f"{dir_path_content} does'nt exist")
    if not os.path.isdir(dir_path_content):
        raise ValueError(f"{dir_path_content} is no directory")
    if not os.path.exists(template_path):
        raise ValueError(f"{template_path} does'nt exist")
    if not os.path.isfile(template_path):
        raise ValueError(f"{template_path} is no file")
    dest_path_parent = os.path.dirname(dest_dir_path)
    os.makedirs(dest_path_parent,exist_ok=True)

    listing = crawl_dir(dir_path_content)
    for l in listing:
        from_path = f"{dir_path_content}/{l}"
        if os.path.isfile(from_path) and l.endswith(".md"):
            markdown =""
            template=""
            with open(from_path, "r") as f:
                markdown = f.read()
            with open(template_path,"r") as f2:
                template =f2.read()
                
            title = extract_title(markdown)
            html_blocks = markdown_to_html_node(markdown)

            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html_blocks.to_html())
            template = template.replace('href="/', f'href="{base_path}')
            template = template.replace('src="/', f'src="{base_path}')

            new_file_path =f"{dest_dir_path}/{l[:-3]}.html"
            destination = os.path.dirname(new_file_path)
            os.makedirs(destination,exist_ok=True)
            with open(new_file_path, "w") as f3:
                f3.write(template)
        if os.path.isdir(from_path): 
            destination = f"{dest_dir_path}/{l}"
            generate_pages_recursive(from_path, template_path, destination, base_path)