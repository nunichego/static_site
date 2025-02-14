from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node) -> HTMLNode:
    if not isinstance(text_node, TextNode):
        raise ValueError("Expected a Textnode instance")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(text_node.text, "b")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(text_node.text, "i")
    elif text_node.text_type == TextType.CODE:
        return LeafNode(text_node.text, "code")
    elif text_node.text_type == TextType.LINK:
        return LeafNode(text_node.text, "a", {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("invalid TextType")
        