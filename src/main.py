from textnode import TextNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextType
from all_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from block_functions import block_to_block_type, markdown_to_html_node
from pathlib import Path
import os
import shutil
import re
import sys
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    
    source = Path(dir_path_content).resolve()
    destination = Path(dest_dir_path).resolve()
    print("dir path",source)

    contents = os.listdir(path=source)
    files = []
    folders = []
    
#what is my base case?
    # content is from the SRC
    #print("contents:", contents)
    for content in contents:
        full_path = f"{source}/{content}" 
        if os.path.isfile(full_path):
            #print(f"{content} - file")
            if content.endswith(".md"):
                print("Found markdown file")
                print(full_path)
                print("CREATING PAGE")
                no_md = content.strip("md")
                add_html = f"{no_md}html"
                full_dest_path = f"{dest_dir_path}/{add_html}"
                print("generating page:", full_dest_path)
                
                generate_page(full_path, template_path, f"{dest_dir_path}/{add_html}",basepath)

        if os.path.isdir(full_path):
            folder = content
            print(f"{content} - Dir")
            folders.append(folder)
    #only recurse on folders:
    if len(folders) != 0:
        #print("FOLDERS",folders)
        #print("new dest", new_destination)
        for folder in folders:
            new_destination = os.path.join(destination,folder)
            #print("FOLDER", folder)
            new_source = os.path.join(source,folder)
            #print("source", source)
            os.makedirs(new_destination)
            generate_pages_recursive(new_source, template_path, new_destination, basepath)


    else:
        print("NO FOLDERS LEFT TO CHECK")
        return
    

def generate_page(from_path, template_path, dest_path,basepath):
    print("============")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as f:
        markdown_file = f.read()
        #print(content)
    with open(template_path, "r") as f:
        template_file = f.read()
        #print(template_file)

    nodes = markdown_to_html_node(markdown_file)
    string_html = nodes.to_html()
    title = extract_title(markdown_file)
#    print(to_html)
    title_template = template_file.replace("{{ Title }}", title)
    #print(title_template)
    content_template = title_template.replace("{{ Content }}", string_html)
    href_template = content_template.replace('href="/', f'href="{basepath}')
    src_template = href_template.replace('src="/', f'src="{basepath}')

   # print(content_template)
    print("writing to:", dest_path)
    with open(dest_path, "w") as f:
        f.write(src_template)

def extract_title(markdown):
    hash_find = re.findall(r"^# (.+)$", markdown, re.MULTILINE)
    #print(hash_find)
    if hash_find:
        print(hash_find)
        to_strip = hash_find[0]
        strip_hash = to_strip.strip("#")
        
    #print(strip_hash)
        strip = strip_hash.strip()
        print(strip)
        return strip
    else:
        raise Exception("No TITLE")


def copy_recursive(source, destination):
    #cwd = os.getcwd()
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    #base_path = os.path.dirname(cwd)
    #source = os.path.join(base_path,source)
    #destination = os.path.join(base_path, destination)

    #print(f"copying contents from {source}")
    #print(f"copying to {destination}")
    contents = os.listdir(path=source)
    files = []
    folders = []
    
#what is my base case?
    # content is from the SRC
    #print("contents:", contents)
    for content in contents:
        full_path = f"{source}/{content}" 
        if os.path.isfile(full_path):
            #print(f"{content} - file")
            #print("copying to:", destination)
            shutil.copy(full_path, destination)

        if os.path.isdir(full_path):
            folder = content
            #print(f"{content} - Dir")
            #new_destination =os.path.join(destination,folder)

            folders.append(folder)
    #only recurse on folders:
    if len(folders) != 0:
        #print("FOLDERS",folders)
        #print("new dest", new_destination)
        for folder in folders:
            new_destination = os.path.join(destination,folder)
            #print("FOLDER", folder)
            new_source = os.path.join(source,folder)
            #print("source", source)
            #print("NEW SOURCE", new_source)
            #print("Making directory", new_destination)
            os.makedirs(new_destination)
            copy_recursive(new_source,new_destination)
    else:
        #print("NO FOLDERS LEFT")
        return

            #return copy_recursive(os.path.join(source, folder),new_destination)
            


def move_files(src, dst):
    full_src = Path(src).resolve()
    final_dst = Path(dst).resolve()
    #print(full_src)
    #cwd = os.getcwd()
    #base_path = os.path.dirname(cwd)
    #final_dst = os.path.join(base_path,dst)
    #print(f"Starting path: {base_path}")


    if not os.path.exists(final_dst):
        print("not found, making dir")
        os.mkdir(final_dst)
    else:
        print(f"deleting folder {final_dst}")
        shutil.rmtree(final_dst)
        print("making Folder")
        os.mkdir(final_dst)

    #contents = os.listdir(path=final_src)
    copy_recursive(src, dst)
    #print(contents)
    #for content in contents:
    #    full_path = f"{final_src}/{content}" 
    #    if content == "":
    #        return
    #    if os.path.isfile(full_path):
    #        print(f"{content} - file")
    #    if os.path.isdir(full_path):
    #        print(f"{content} - Dir")
    #        return (src, content)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    move_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)






if __name__ == "__main__":
    main()

"""
Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)

    It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    It should copy all files and subdirectories, nested files, etc.
    I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.

"""
