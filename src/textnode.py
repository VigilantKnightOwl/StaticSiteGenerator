from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "Links, in this format: [anchor text](url)"
    IMAGE = "Images, in this format: ![alt text](url)"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type: TextType = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        result = LeafNode(None, text_node.text) 
    elif text_node.text_type == TextType.BOLD:
        result = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        result = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        result = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("A URL is required for a link")
        if text_node.text is None:
            raise ValueError("Anchor text is required for an image")
        props: dict[str, str] = {"href": text_node.url}
        result = LeafNode("a", f"[{text_node.text}]", props)
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("A URL is required for an image")
        result = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("No valid Text Type found")
    return result

#node = TextNode("This is a Link", TextType.LINK, "https://www.boot.dev")
#html_node = text_node_to_html_node(node)
#print(text_node_to_html_node(node))

node = TextNode("This is an Image", TextType.IMAGE, "https://www.google.com")
html_node = text_node_to_html_node(node)
print(text_node_to_html_node(node))

