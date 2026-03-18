
import os
import sys

from .file_and_directory import copy_directory_recursively
from .markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    html_string = markdown_to_html_node(markdown_content).to_html()
    html_title = extract_title(markdown_content)
    
    template_content = template_content.replace("{{ Title }}", html_title)
    template_content = template_content.replace("{{ Content }}", html_string)
    if basepath:
        template_content = template_content.replace('href="/', f'href="{basepath}')
        template_content = template_content.replace('src="/', f'src="{basepath}')
                                 
    destination_parent = os.path.dirname(dest_path)
    if destination_parent and not os.path.exists(destination_parent):
        os.makedirs(destination_parent)

    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for item in os.listdir(dir_path_content):
        item_path_content = os.path.join(dir_path_content, item)
        item_path_dest = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_path_content) and item.endswith(".md"):
            generate_page(item_path_content, template_path, item_path_dest.replace(".md", ".html"))
        elif os.path.isdir(item_path_content):
            generate_pages_recursive(item_path_content, template_path, item_path_dest, basepath)

def main():
    basepath = sys.argv

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(project_root, "static")
    destination_dir = os.path.join(project_root, "docs")
    copy_directory_recursively(source_dir, destination_dir)

    generate_pages_recursive(
        os.path.join(project_root, "content"), 
        os.path.join(project_root, "template.html"), 
        destination_dir,
        basepath
    )



if __name__ == "__main__":
    main()