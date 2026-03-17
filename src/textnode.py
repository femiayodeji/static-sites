import re
from enum import Enum
from typing import Optional

from .htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url ==  other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "":
        raise ValueError("Delimiter cannot be empty")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        for index, section in enumerate(sections):
            if index % 2 == 0:
                if section:
                    new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for alt_text, url in matches:
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index == -1:
                continue
            
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt_text}]({url})")
        
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for link_text, url in matches:
            start_index = node.text.find(f"[{link_text}]({url})", last_index)
            if start_index == -1:
                continue
            
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = start_index + len(f"[{link_text}]({url})")
        
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
    
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
