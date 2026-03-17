import unittest

from src.markdown import extract_title, markdown_to_blocks, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_no_newlines(self):
        md = "This is a **single block** of text with no newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a **single block** of text with no newlines"])

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_and_quote(self):
        md = """
# Heading with **bold**

> Quoted _text_ here
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with <b>bold</b></h1><blockquote>Quoted <i>text</i> here</blockquote></div>",
        )

    def test_lists(self):
        md = """
- apple
- banana

1. first
2. second
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>apple</li><li>banana</li></ul><ol><li>first</li><li>second</li></ol></div>",
        )
    
    def test_extract_title(self):
        text = "# Hello"
        title = extract_title(text)
        self.assertEqual(title, "Hello")
        
        text = "## Not a title"
        with self.assertRaises(ValueError):
            extract_title(text)

if __name__ == "__main__":
    unittest.main()