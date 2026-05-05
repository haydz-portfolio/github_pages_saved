from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type,url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, tn):
        return (
            self.text_type == tn.text_type
            and self.text == tn.text
            and self.url == tn.url
            )
    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type!r}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("NOT")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": "", "alt":"" })

   # def text_node_to_html_node(text_node):
   #     if text_node.text_type not in TextType:
   #         raise Exception("NOT")


