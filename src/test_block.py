import unittest
from block_functions import block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode


class TestMarkDownToHTML(unittest.TestCase):
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
        md = """```
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
 #   def test_heading(self):
#        md = """
#### Heading 4

#this is text

#text again

#- abc
#- def
#3
#1. test
#2. abc
#
#> HELLO THERE
#> WOW
#
#```\ntest _italic_ **bold**\n```
#"""
        

       # node = markdown_to_html_node(md)
       # html = node.to_html()
        #self.assertEqual(
          #  html,
         #   "<h1>Heading 1</h1>",
        #)


class TestBlockTypes(unittest.TestCase):

    def test_block_heading(self):
        block = "### HEADING 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)


    def test_code_block(self):
        block = """
```
this is code
```
"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_quote_block(self):
        block = """> test
> qqq
> LOL
"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_block(self):
        block = """- abc
- abc
- ac
"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_block(self):
        block = """1. test
2. test
3. test"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)



if __name__ == "__main__":
    unittest.main()
