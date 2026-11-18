import sys
from file_management import migrate_files, generate_page, generate_pages_recursive

#text_type = TextType.LINK
#def main(text: str, text_type_name: str, anchor_url: str):
#    text_type = TextType[text_type_name]
        
#   return TextNode(text, text_type, anchor_url)

#print(main("This is some anchor text", "LINK", "https://www.boot.dev"))

#node = TextNode("This is a text node", TextType.TEXT)
#print(node.text_node_to_html_node())

#node = TextNode("This is a text node", TextType.TEXT)
#html_node = text_node_to_html_node(node)
#print(html_node)
#self.assertEqual(html_node.tag, None)
#self.assertEqual(html_node.value, "This is a text node")

# Run the following CLI to start a browser (currently handled in main.sh):
'''
cd public
python3 -m http.server 8888
'''

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

backup_path, log_path = migrate_files("static", "docs")
print(f"Backup: {backup_path}")
print(f"Log: {log_path}")

generate_pages_recursive(basepath,
                         "content", 
                         "template.html", 
                         "docs",
                        )
