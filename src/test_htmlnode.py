import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_to_html_raised(self):
        node = HTMLNode("h1", "Sample Text", None, None)
        with self.assertRaises(NotImplementedError): 
            string = node.to_html()

      
    def test_props_to_html_n1a(self):
        child_node1a = HTMLNode("a", "href='https://www.boot.dev'", None, {"href": "https://www.google.com"})
        print(repr(child_node1a))
        expected = ' href="https://www.google.com"'
        result = child_node1a.props_to_html()
        self.assertEqual(expected, result)
 
    def test_props_to_html_n1(self):        
        child_node1a = HTMLNode("a", "href='https://www.boot.dev'", None, {"href": "https://www.google.com"})
        child_node1 = HTMLNode("body", "Main Text", [child_node1a], {"a": "href='https://www.boot.dev'", "href": "https://www.google.com",})
        expected = ' a="href=''https://www.boot.dev''" href="https://www.google.com"'
        result = child_node1.props_to_html()
        self.assertNotEqual(expected, result)

                    
    def test_props_to_html_n(self):
        child_node1a = HTMLNode("a", "href='https://www.boot.dev'", None, {"href": "https://www.google.com"})
        child_node1 = HTMLNode("body", "Main Text", [child_node1a], {"a": "href='https://www.boot.dev'", "href": "https://www.google.com",})
        node = HTMLNode("h1", "Sample Text", [child_node1], None)
        expected = None
        result = node.props_to_html()
        self.assertNotEqual(expected, result)

    def test_leaf_to_html_pa(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_pb(self):
        node = LeafNode("a", "Main Text", {"a": "href='https://www.boot.dev'", "href": "https://www.google.com"})
        print(node.to_html())
        self.assertEqual(node.to_html(), """<a a="href='https://www.boot.dev'" href="https://www.google.com">Main Text</a>""")

    def test_leaf_to_html_pc(self):
        node = LeafNode("a", "Main Text", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Main Text</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

     
    def test_to_html_with_grandchildren_and_props(self):   
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"a": "href='https://www.boot.dev'", "href": "https://www.google.com",})
        self.assertEqual(
            parent_node.to_html(),
            '''<div><span><b>grandchild</b></span></div> a="href='https://www.boot.dev'" href="https://www.google.com"'''
        )


    def test_text_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_text_2(self):      
        with self.assertRaises(AttributeError): 
            node = TextNode("This is a text node", TextType.ERROR)  
            html_node = text_node_to_html_node(node)

    def test_text_3(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD text node")
        self.assertEqual(html_node.props, None)

    def test_text_4(self):
        node = TextNode("This is an ITALIC text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an ITALIC text node")
        self.assertEqual(html_node.props, None)

    def test_text_5(self):
        node = TextNode("This is a CODE text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a CODE text node")
        self.assertEqual(html_node.props, None)
        
    def test_text_6(self):
        node = TextNode("This is a Link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "[This is a Link]")
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})
        
    def test_text_7(self):
        node = TextNode("This is an Image", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://www.google.com', 'alt': 'This is an Image'})
        
        

if __name__ == "__main__":
    unittest.main()
