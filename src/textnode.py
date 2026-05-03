from enum import Enum
from htmlnode import LeafNode

"""text (plain)
    **Bold text**
    _Italic text_
    `Code text`
    Links, in this format: [anchor text](url)
    Images, in this format: ![alt text](url)"""

class TextType(Enum):
    
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES =  "images"

class TextNode():
    def __init__(self, text, text_type:TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value):
        if value.text != self.text:
            return False
        if value.text_type != self.text_type:
            return False
        if value.url != self.url:
            return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGES:
            return LeafNode("img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text_node.text_type invalid")

