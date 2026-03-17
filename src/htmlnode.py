from typing import Optional


class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[list] = None, props: Optional[dict] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError("Error: HTMLNode is an abstract class and cannot be instantiated directly.")

    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: Optional[str], props: Optional[dict] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag is None:
            if self.value is None:
                raise ValueError("Error: LeafNode must have either a tag or a value.")
            return self.value
        if self.value is None:
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, props: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag: Optional[str], children: Optional[list], props: Optional[dict] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: All parent nodes must have a tag.")
        if not self.children:
            raise ValueError("Error: All parent nodes must have at least one child.")
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"