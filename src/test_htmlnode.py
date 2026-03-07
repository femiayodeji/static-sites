import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello World", [HTMLNode("p", "This is a paragraph.")], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "This is a paragraph.")
        self.assertEqual(node.props["class"], "container")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("p", "Hello, world!", {"class": "text"})
        self.assertEqual(node2.to_html(), '<p class="text">Hello, world!</p>')

        node3 = LeafNode(None, "Hello, world!")
        self.assertEqual(node3.to_html(), "Hello, world!")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )    

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"class": "text"})
        parent_node = ParentNode("div", [child_node], {"id": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="container"><span class="text">child</span></div>',
        )