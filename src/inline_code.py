import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid Markdown: delimiter is not closed")
        for index, part in enumerate(parts):
            if part =="":
                continue
            part_type = text_type if index % 2 else TextType.TEXT
            new_nodes.append(TextNode(part, part_type))

    return new_nodes

    
    
    #raise Exception("Error: invalid Markdown syntax")


#node = TextNode("This is bold text with a **bold**", TextType.TEXT)
#print(split_nodes_delimiter([node], "**", TextType.BOLD))

def extract_markdown_images(text) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

#text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]


def extract_markdown_links(text) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


# text: list[str, str] = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# result = extract_markdown_links(text)
# print(extract_markdown_links(text))
# for alt_text, url in result:
#     print(f"[{alt_text}]({url})")
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]



def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for alt_text, url in matches:
            sections = original_text.split(sep=f"![{alt_text}]({url})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

#node = TextNode(
#    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#    TextType.TEXT,
#)
#new_nodes = split_nodes_image([node])
#print(split_nodes_image([node]))
#node = TextNode(
#            "Tis is an ![image](https://i.imgur.com/zjjcJKZ.png)",
#            TextType.TEXT,
#        )
#print(split_nodes_image([node]))

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for alt_text, url in matches:
            sections = original_text.split(sep=f"[{alt_text}]({url})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
'''
node = TextNode(
    "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
    TextType.TEXT,
)
print(split_nodes_link([node]))

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
print(split_nodes_link([node]))
'''

def text_to_textnodes(text: str) -> list[TextNode]:
     nodes = [TextNode(text, TextType.TEXT)]
     image_nodes = split_nodes_image(nodes)
     link_nodes = split_nodes_link(image_nodes)
     bold_nodes = split_nodes_delimiter(link_nodes, "**", TextType.BOLD)
     italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
     final_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
     return final_nodes


#text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#print(text_to_textnodes(text))

#[TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" and an ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev")]
# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes: list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
# print(new_nodes)