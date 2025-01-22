import os
import shutil

def copy_src_to_dest(src, dest):
    if not os.path.exists(src):
        raise ValueError("Source directory does not exist: " + src)
    if os.path.exists(dest):
        print("Removing everything from dest")
        shutil.rmtree(dest)
    print("Creating destination directory: " + dest)
    os.mkdir(dest)
    list = os.listdir(src)
    print(list)
    for item in list:
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            print("Copying file: " + item)
            shutil.copy(src_path, dest)
        else:
            dest_path = os.path.join(dest, item)
            print(f"Copying directory: {src_path} to {dest_path}")
            copy_src_to_dest(src_path, dest_path)
    return None
