import os
import shutil   

from markdown_functions import markdown_to_html_node, extract_title
from htmlnode import *

#crea...lder creates list of pathes of all the files inside of it based on an input path
def create_paths_for_elements_in_folder(path):
    paths = []
    for object in os.listdir(path):
        full_path = os.path.join(path, object)
        if os.path.isfile(full_path):
            paths.append(full_path)
        else:
            subdirectory_paths = create_paths_for_elements_in_folder(full_path)
            paths.extend(subdirectory_paths)
    return paths

#stat...blic removes public folder, creates new empty one and copies all from static to it
def static_to_public():

    source_dir = 'static'
    dest_dir = 'public'

    if not os.path.exists(source_dir):
        raise Exception("source directory wasn't found")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    
    for source_path in create_paths_for_elements_in_folder(source_dir):
        rel_path = os.path.relpath(source_path, source_dir)
        dest_path = os.path.join(dest_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(source_path, dest_path)

    return

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    template_file = open(template_path, "r")
    template = template_file.read()
    markdown_file.close()
    template_file.close()

    html_from_markdown = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    template.replace('Title', page_title)

    page = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_from_markdown)
    page_file = open(dest_path, "w")
    page_file.write(page)
    page_file.close()

    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for source_path in create_paths_for_elements_in_folder(dir_path_content):
        if source_path[-3:] == ".md":
            rel_path = os.path.relpath(source_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, rel_path).replace(".md",".html")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(source_path, template_path, dest_path)

    return


