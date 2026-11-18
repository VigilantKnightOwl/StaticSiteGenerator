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

# Run the following CLI to start a browser:
'''
cd public
python3 -m http.server 8888
'''
backup_path, log_path = migrate_files("static", "public")
print(f"Backup: {backup_path}")
print(f"Log: {log_path}")

'''
generate_page("content/index.md", 
              "template.html", 
              "public/index.html",
              )

generate_page("content/blog/glorfindel/index.md",
              "template.html",
              "public/blog/glorfindel/index.html",
)

generate_page("content/blog/tom/index.md",
              "template.html",
              "public/blog/tom/index.html",
)

generate_page("content/blog/majesty/index.md",
              "template.html",
              "public/blog/majesty/index.html",
)

generate_page("content/contact/index.md",
              "template.html",
              "public/contact/index.html",
)


    # template_path: str | Path,
    # dest_path: str | Path,
    # )
'''

generate_pages_recursive("content", 
                         "template.html", 
                         "public",
                        )
