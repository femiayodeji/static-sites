
import os

from file_and_directory import copy_directory_recursively
from markdown import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    html_string = markdown_to_html_node(markdown_content).to_html()
    html_title = extract_title(markdown_content)
    
    template_content = template_content.replace("{{ title }}", html_title)
    template_content = template_content.replace("{{ content }}", html_string) # type: ignore

    with open(dest_path, "w") as f:
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))
        f.write(template_content)


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(project_root, "static")
    destination_dir = os.path.join(project_root, "public")
    copy_directory_recursively(source_dir, destination_dir)

    generate_page(
        os.path.join(project_root, "content", "index.md"),
        os.path.join(project_root, "", "template.html"),
        os.path.join(destination_dir, "index.html"),
    )

if __name__ == "__main__":
    main()