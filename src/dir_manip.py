import os
import shutil

def get_list_dir_from(path):
    if not os.path.exists(path):
        raise ValueError(f"{path} doesn't exist")
    return os.listdir(path)

def clear_dir(path):
    if not os.path.exists(path):
        raise ValueError(f"{path} doesn't exist")

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            shutil.rmtree(full_path)  # supprime sous-dossier
        else:
            os.remove(full_path)      # supprime fichier
    #print(f"{path} - content cleared")

def copy_dir(src, dest):
    if not os.path.isdir(src):
        raise ValueError(f"src path : {src} is not a directory")
    if not os.path.isdir(dest):
        raise ValueError(f"dest path : {dest} is not a directory")
    
    shutil.copytree(src,dest, dirs_exist_ok=True)

def crawl_dir(dir):
    if not os.path.exists(dir):
        raise ValueError(f"{dir} doesn't exist")
    listing = os.listdir(dir)
    return listing
    