
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("Hello World", TextType.LINK, "https://example.com")
    print(text_node)

    html_node = HTMLNode("div", children=[HTMLNode("p", value="This is a paragraph.")], props={"class": "container"})
    print(html_node)

    print("-" * 20)
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.to_html())

if __name__ == "__main__":
    main()