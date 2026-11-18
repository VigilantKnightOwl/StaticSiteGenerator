import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_code import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph block"           # <p>
    HEADING = "heading block"               # <h{1-6}>
    CODE = "code block"                     # <code>
    QUOTE = "quote block"                   # <blockquote>
    UNORDERED_LIST = "unordered_list block" # <ul>
    ORDERED_LIST = "ordered_list block"     # <ol>

def markdown_to_blocks(markdown: str) -> list[str]:
    if not isinstance(markdown, str):
        raise ValueError("invalid input. parameter must be a text string")
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip() #"\n".join(line.lstrip() for line in block.splitlines()).
        filtered_blocks.append(block)
    return filtered_blocks
'''
md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """

    
md = ""    
blocks = markdown_to_blocks(md)
print(blocks)

print(type(""))
print(markdown_to_blocks(""))
'''

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].strip() == "```" and lines[-1].strip() == "```" :
        return BlockType.CODE
    elif len(lines) > 1 and lines[0].startswith("```") and not lines[0].strip() == "```":
        raise ValueError(f"invalid markdown. Code block delimeter not on initial line by itself at: {lines[0]}")
    elif len(lines) > 1 and lines[0].strip() == "```":
        if not re.findall("```", lines[-1]):  # first line CODE delimiter present, missing from final line 
            raise ValueError(f'invalid markdown. missing Code block closing delimeter at: "{lines[-1]}"')
        if (lines[-1].startswith("```") and not lines[-1].endswith("```")) or (not lines[-1].startswith("```") and lines[-1].endswith("```")): #delimiter present on final line, but not alone
            raise ValueError(f'invalid markdown. Code block delimeter not on final line by itself at: "{lines[-1]}"')
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                raise ValueError(f'invalid markdown. each new line of a quote must start with ">": {line}')
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                raise ValueError(f'invalid markdown. each new line of unordered lists must start with "- ": {line}')
        return BlockType.UNORDERED_LIST
    if re.match(r"(\d+). ", block):
        for line in lines:
            line_start = re.findall(r"^\d+\. ", line)
            if len(line_start) == 0:
                raise ValueError('invalid markdown. each new line of ordered lists must start with a number followed by "."')
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
#print(block_to_block_type("# item 1 \n##. item 2 \n#######item 3"))
#print(block_to_block_type('```\nre.findall(r"(nd+). ", block)\n```'))
#print(block_to_block_type('```\nre.findall(r"(nd+). ", block)``` and ```print("hello")\n```'))
#print(block_to_block_type('```re.findall(r"(nd+). ", block)``` and ```print("hello")\n```'))
#print(block_to_block_type('```\nre.findall(r"(nd+). ", \nblock)'))
#print(block_to_block_type('```\nre.findall(r"(nd+). ", block)``` and ```print("hello")```'))
#print(block_to_block_type('```re.findall(r"(nd+). ", block)'))
#print(block_to_block_type("> item 1 \n>. item 2 \n>item 3"))
#print(block_to_block_type("> item 1 \n>. item 2 \n>item 3\n4. item 4"))
#print(block_to_block_type("- item 1 \n- item 2 \n- item 3"))
#print(block_to_block_type("- item 1 \n- item 2 \n- item 3 \n - item 4"))
#print(block_to_block_type("1. item 111 \n211. item 2 \n113. item 3 \n4. item 4"))
#print(block_to_block_type("111. item 1 \n112. item 2 \n323. item 3 \n- item 4"))
#print(block_to_block_type("This is just a para. of text. \n#######item 3 ```re.findall(r'(nd+). ', block)``` > item 1 \n>. item 2 \n>item 3 - item 1 \n- item 2 \n- item 3 1. item 111 \n211. item 2 \n113. item 3 \n4. item 4  "))

#(?<!.*?)



def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    new_line: str = ""
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise ValueError("No level 1 Header text found")

#line = extract_title("# Hello")
#print(line)


# md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

# md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and \n```\ncode\n```\n here

# """


#node = markdown_to_html_node(md)
#html = node.to_html()
#print(html)


