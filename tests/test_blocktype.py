import unittest
from src.blocktype import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        block = "- This is an unordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_code(self):
        block = "```This is a code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


if __name__ == "__main__":
    unittest.main()


