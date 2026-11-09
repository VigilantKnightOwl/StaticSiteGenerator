from textnode import TextType, TextNode
from enum import Enum
#text_type = TextType.LINK
#def main(text: str, text_type_name: str, anchor_url: str):
#    text_type = TextType[text_type_name]
        
#   return TextNode(text, text_type, anchor_url)

#print(main("This is some anchor text", "LINK", "https://www.boot.dev"))

#node = TextNode("This is a text node", TextType.TEXT)
#print(node.text_node_to_html_node())

node = TextNode("This is a text node", TextType.TEXT)
html_node = text_node_to_html_node(node)
print(html_node)
#self.assertEqual(html_node.tag, None)
#self.assertEqual(html_node.value, "This is a text node")