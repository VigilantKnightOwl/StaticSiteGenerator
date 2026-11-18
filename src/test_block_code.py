import unittest
from block_code import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title


class TestBlockCode(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = ""    
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_markdown_to_blocks_3(self):        
        with self.assertRaises(ValueError):
            md = [""]    
            blocks = markdown_to_blocks(md)


        
    def test_block_to_block_type_HEADING_1(self):
        md = "# item 1 \n##. item 2 \n#######item 3     "
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )
        
    def test_block_to_block_type_CODE_2a(self):
        md = '```\nre.findall(r"(nd+). ", block)\n```'
        print(md)
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.CODE
        )
        
    def test_block_to_block_type_CODE_2b(self):
        md = '```\nre.findall(r"(nd+). ", block)``` and ```print("hello")\n```'
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.CODE
        )
        
    def test_block_to_block_type_CODE_2c(self):     
        with self.assertRaises(ValueError):
            md = '```\nre.findall(r"(nd+). ", block)``` and ```print("hello")```'
            block_type: BlockType = block_to_block_type(md)
        
    def test_block_to_block_type_CODE_2d(self):     
        with self.assertRaises(ValueError):
            md = '```\nre.findall(r"(nd+). ", \nblock)'
            block_type: BlockType = block_to_block_type(md)
        
    def test_block_to_block_type_CODE_2e(self):  
        md = '```re.findall(r"(nd+). ", block)```'
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_CODE_2f(self):     
        with self.assertRaises(ValueError):
            md = '```re.findall(r"(nd+). ", block)``` and ```print("hello")\n```'
            block_type: BlockType = block_to_block_type(md)
        
    def test_block_to_block_type_QUOTE_3a(self):
        md = "> item 1 \n>. item 2 \n>item 3     "
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.QUOTE
        )
        
    def test_block_to_block_type_QUOTE_3b(self):     
        with self.assertRaises(ValueError):
            md = "> item 1 \n>. item 2 \n>item 3\n4. item 4"
            block_type: BlockType = block_to_block_type(md)
        
    def test_block_to_block_type_UNORDERED_4a(self):
        md = "- item 1 \n- item 2 \n- item 3     "
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.UNORDERED_LIST
        )
        
    def test_block_to_block_type_UNORDERED_4b(self):     
        with self.assertRaises(ValueError):
            md = "- item 1 \n- item 2 \n- item 3 \n - item 4"
            block_type: BlockType = block_to_block_type(md)
        
    def test_block_to_block_type_ORDERED_5a(self):
        md = "1. item 111 \n211. item 2 \n113. item 3 \n4. item 4     "
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.ORDERED_LIST
        )
        
    def test_block_to_block_type_ORDERED_5b(self):     
        with self.assertRaises(ValueError):
            md = "111. item 1 \n112. item 2 \n323. item 3 \n- item 4"
            block_type: BlockType = block_to_block_type(md)
        
    def test_block_to_block_type_PARAGRAPH_6(self):
        md = "This is just a para. of text. \n#######item 3 ```re.findall(r'(nd+). ', block)``` > item 1 \n>. item 2 \n>item 3 - item 1 \n- item 2 \n- item 3 1. item 111 \n211. item 2 \n113. item 3 \n4. item 4      "
        block_type: BlockType = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


        def test_extract_title_1a(self):
            md = "# Hello"
            line = extract_title(md)
            self.assertEqual(
                line, "Hello"
            )


        def test_extract_title_1b(self):
            md = "Hi, \n# Hello\n how are you?"
            line = extract_title(md)
            self.assertEqual(
                line, "Hello"
            )

        
        def test_extract_title_1c(self):     
            with self.assertRaises(ValueError):
                md = "Hello"
                line = extract_title(md)

        
        def test_extract_title_1d(self):     
            with self.assertRaises(ValueError):
                md = "## Hello"
                line = extract_title(md)

        
        def test_extract_title_1e(self):     
            with self.assertRaises(ValueError):
                md = "#Hello"
                line = extract_title("md")


if __name__ == "__main__":
    unittest.main()