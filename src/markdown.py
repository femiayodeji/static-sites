from textwrap import dedent

from .textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node
from .blocktype import BlockType, block_to_block_type
from .htmlnode import ParentNode



def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != "", blocks))
    return blocks


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def _paragraph_to_html_node(block):
    paragraph_text = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", text_to_children(paragraph_text))


def _heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    heading_level = min(max(level, 1), 6)
    heading_text = block[level:].strip()
    return ParentNode(f"h{heading_level}", text_to_children(heading_text))


def _code_to_html_node(block):
    code_text = block[3:-3]
    if code_text.startswith("\n"):
        code_text = code_text[1:]
    code_text = dedent(code_text)
    code_child = text_node_to_html_node(TextNode(code_text, TextType.TEXT))
    code_node = ParentNode("code", [code_child])
    return ParentNode("pre", [code_node])


def _quote_to_html_node(block):
    quote_lines = []
    for line in block.split("\n"):
        if line.startswith(">"):
            quote_lines.append(line[1:].strip())
        else:
            quote_lines.append(line.strip())
    quote_text = " ".join(quote_lines)
    return ParentNode("blockquote", text_to_children(quote_text))


def _unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        item_text = line[2:].strip()
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)


def _ordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        item_text = line.split(". ", 1)[1].strip()
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(_paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            html_nodes.append(_heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            html_nodes.append(_code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(_quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(_unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(_ordered_list_to_html_node(block))
        else:
            raise ValueError(f"Unsupported block type: {block_type}")

    return ParentNode("div", html_nodes)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("#") and block.count("#") == 1:
            return block.lstrip("#").strip()
    raise ValueError("No title found in markdown")


