from dir_manip import *
import os 
path = "./content"
listing = crawl_dir(path)
for l in listing: 
    complete_path = f"{path}/{l}"
    dest_path_parent = os.path.dirname(complete_path)
    print(f"complete_path = {complete_path}")
    print(f"dest_path_parent = {dest_path_parent}")
    if os.path.isfile(complete_path):
        print(f"{complete_path}")
        if l.endswith(".md"):
            print(f"{l} is a md file!")
    if os.path.isdir(complete_path):
        print("we need to go deeper!")        
        print(f"complete_path = {complete_path}")
        print(f"dest_path_parent = {dest_path_parent}")
        new_listing =  crawl_dir(complete_path)
        for n in new_listing:
            print(n)