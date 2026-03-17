import unittest
from src.markdown import text_to_textnodes
from src.textnode import TextNode, TextType

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        assert result == expected

    def test_text_to_textnode_no_markdown(self):
        text = "This is a plain text with no markdown"
        expected = [
            TextNode("This is a plain text with no markdown", TextType.TEXT)
        ]
        result = text_to_textnodes(text)
        assert result == expected

    def test_text_to_textnode_only_markdown(self):
        text = "**bold** _italic_ `code` ![image](https://i.imgur.com/fJRm4Vk.jpeg) [link](https://boot.dev)"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        assert result == expected

if __name__ == "__main__":
    unittest.main()