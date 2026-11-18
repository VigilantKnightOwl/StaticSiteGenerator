import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_code import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)
        
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is not a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)
        
    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)


    def test_text_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_text_2(self):      
        with self.assertRaises(ValueError): 
            node = TextNode("This is a text node", None)  
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


    def test_inlinetext_1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
        for text_node in new_nodes:
            if text_node.text == "This is text with a ":                
                self.assertEqual(text_node.text, "This is text with a ")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            if text_node.text == "code block":                
                self.assertEqual(text_node.text, "code block")
                self.assertEqual(text_node.text_type, TextType.CODE)
            if text_node.text == " word":                
                self.assertEqual(text_node.text, " word")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            self.assertEqual(text_node.url, None)

    def test_inlinetext_1a(self):
        node = TextNode("This is text with a `code block` word", TextType.BOLD)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
        for text_node in new_nodes:              
                self.assertEqual(text_node.text, "This is text with a `code block` word")
                self.assertEqual(text_node.text_type, TextType.BOLD)
                self.assertEqual(text_node.url, None)

    def test_inlinetext_2(self):
        node = TextNode("This is bold text with a **bold** word", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD)
        for text_node in new_nodes:
            if text_node.text == "This is bold text with a ":                
                self.assertEqual(text_node.text, "This is bold text with a ")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            if text_node.text == "bold":                
                self.assertEqual(text_node.text, "bold")
                self.assertEqual(text_node.text_type, TextType.BOLD)
            if text_node.text == " word":                
                self.assertEqual(text_node.text, " word")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            self.assertEqual(text_node.url, None)

    def test_inlinetext_2a(self):
        node = TextNode("This is bold text with a **bold**", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD)
        for text_node in new_nodes:
            if text_node.text == "This is bold text with a ":                
                self.assertEqual(text_node.text, "This is bold text with a ")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            if text_node.text == "bold":                
                self.assertEqual(text_node.text, "bold")
                self.assertEqual(text_node.text_type, TextType.BOLD)
            if text_node.text == " word":                
                self.assertEqual(text_node.text, " word")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            self.assertEqual(text_node.url, None)

    def test_inlinetext_3(self):
        node = TextNode("This is italic text with an _italic_ word", TextType.TEXT)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "_", TextType.ITALIC)
        for text_node in new_nodes:
            if text_node.text == "This is italic text with a ":                
                self.assertEqual(text_node.text, "This is italic text with a ")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            if text_node.text == "italic":                
                self.assertEqual(text_node.text, "italic")
                self.assertEqual(text_node.text_type, TextType.ITALIC)
            if text_node.text == " word":                
                self.assertEqual(text_node.text, " word")
                self.assertEqual(text_node.text_type, TextType.TEXT)
            self.assertEqual(text_node.url, None)


    def test_extract_markdown_images_1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with a ![r i c k roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("r i c k roll", "https://i.imgur.com/aKaOqIh.gif"),("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_3(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    def test_split_images_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


    def test_split_images_2(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


    def test_split_links_1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )


    def test_split_links_2(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("This is ", TextType.TEXT), 
                              TextNode("text", TextType.BOLD), 
                              TextNode(" with an ", TextType.TEXT), 
                              TextNode("italic", TextType.ITALIC), 
                              TextNode(" word and a ", TextType.TEXT), 
                              TextNode("code block", TextType.CODE), 
                              TextNode(" and an ", TextType.TEXT), 
                              TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                              TextNode(" and a ", TextType.TEXT),
                              TextNode("link", TextType.LINK, "https://boot.dev")],
            new_nodes,
        )

    def test_text_to_textnodes_2(self):
        with self.assertRaises(ValueError):
            text = "This is **text** with an _italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            new_nodes = text_to_textnodes(text)
        

if __name__ == "__main__":
    unittest.main()


