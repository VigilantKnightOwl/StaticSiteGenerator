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
        
        

if __name__ == "__main__":
    unittest.main()
