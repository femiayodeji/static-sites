from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block[0].isdigit() and block[1:3] == ". ":
        return BlockType.ORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
