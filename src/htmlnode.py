from enum import Enum


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Method not yet implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join(f' {name}="{value}"' for name, value in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props_to_html()}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            tag,
            value,
            None,
            props
        )
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("ERROR: No Value provided")
        if self.tag is None:
            return f"{self.value}"
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        #return "".join(f' <{self.tag} {attrib_name}="{attrib_value}">{self.value}</{self.tag}>' for attrib_name, attrib_value in self.props.items())
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[LeafNode],
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ERROR: No tag provided")
        if self.children is None:
            raise ValueError("ERROR: No child node provided")
        child_node_str: str = ""
        for child in self.children:
            child_node_str += child.to_html()
        return f"<{self.tag}>{child_node_str}</{self.tag}>{self.props_to_html()}"
        #if self.props is None:
        #    return f"<{self.tag}>{self.value}</{self.tag}>"
        #return "".join(f' <{self.tag} {attrib_name}="{attrib_value}">{self.value}</{self.tag}>' for attrib_name, attrib_value in self.props.items())
        #return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
        
        

'''
child_node1a = HTMLNode("a", "href='https://www.boot.dev'", None, {"href": "https://www.google.com"})
child_node1 = HTMLNode("body", "Main Text", [child_node1a], {"a": "href='https://www.boot.dev'", "href": "https://www.google.com",})
node = HTMLNode("h1", "Sample Text", [child_node1], None)
print(repr(node))
print(node.props_to_html())
print(repr(child_node1))
print(child_node1.props_to_html())
print(repr(child_node1a))
print(child_node1a.props_to_html())
'''
#print(LeafNode("p", "This is a paragraph of text.").to_html())
#print(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html())
#print(LeafNode("p", "Hello, world!").to_html())

#node = LeafNode("a", "Main Text", {"a": "href='https://www.boot.dev'", "href": "https://www.google.com"})
#print(node.to_html())

#grandchild_node = LeafNode("b", "grandchild")
#child_node = ParentNode("span", [grandchild_node])
#parent_node = ParentNode("div", [child_node], {"a": "href='https://www.boot.dev'", "href": "https://www.google.com",})

#child_node = LeafNode("span", "child")
#parent_node = ParentNode("div", [child_node])
#print(parent_node.to_html())
