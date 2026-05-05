import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from all_functions import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote" 
    UNORDERED_LIST = "unorded_list"
    ORDERED_LIST = "ordered_list"

def text_to_children(text):
    #print(f"text{text}")
    nodes = []
    text_nodes = text_to_textnodes(text)
    #print("TEXTGNODES")
    #print("Text Nodes", text_nodes)
    for text_node in text_nodes:
        nodes.append(text_node_to_html_node(text_node))
    #print("nodes", nodes)
    return nodes

def markdown_to_html_node(markdown):
 #   print("hello")if
 #   print(markdown)
 #   print("TEST")
    blocks = markdown_to_blocks(markdown)
 #   print("blocks")
 #   print(blocks)
    formatted_nodes = []
    formatted = {}
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        #print(f"BLOCK: {repr(block)}")
        #print(f"TYPE: {block_type}")
        #block_type = block_to_block_type(block)
        #print(f"BLOCK: {repr(block)}")
        #print(f"TYPE: {block_type}")
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
           # hash_find = re.findall(r'```(#*?)```', block,  re.DOTALL)
            hash_find = re.findall(r'(^#+)', block)
            #print("hash_find)", hash_find)
            heading_number = len(hash_find[0])
            #print(heading_number)
            heading_level = f"h{heading_number}"
            strip_1= block.strip("#")
            #print("strip",strip_1)
            #print(strip_1)
            strip_2 = strip_1.strip()
            result = text_to_children(strip_2)
            #print("leaf", result)
            #html_nodes.append(leaf)
            convert_parent_node = ParentNode(heading_level,result)
            #print(convert_parent_node)
            html_nodes.append(convert_parent_node)
        if block_type == BlockType.PARAGRAPH:
            #print(block_type)
            #print(block)
            result = text_to_children(block.replace("\n"," "))
            #print("result",result)
            convert_parent_node = ParentNode("p",result)


            #print(convert_parent_node)
            html_nodes.append(convert_parent_node)
        if block_type  == BlockType.UNORDERED_LIST:
            #print("unordered")
            #print(block)
            leaf_nodes = []
            split_lines = block.split("\n")
            for line in split_lines:
                #print("LINE", line)
                strip_dash = line.strip("-")
                strip_space = strip_dash.strip()
                #print(strip_space)
                result = text_to_children(strip_space)
                leaf_nodes.append(result)
            #print("LEAFNODES", leaf_nodes)
            unordered_parent_nodes = []
            for node in leaf_nodes:
                unordered_parent_nodes.append(ParentNode("li", node))
            #print(unordered_parent_nodes)
            convert_parent_node = ParentNode("ul", unordered_parent_nodes)
            html_nodes.append(convert_parent_node)
        if block_type  == BlockType.ORDERED_LIST:
            #print("ordered")
            #print(block)
            leaf_nodes = []
            split_lines = block.split("\n")
            for line in split_lines:
                line = line[2:]
                strip_space = line.strip()
                #print("STRIP",strip_space)
                result = text_to_children(strip_space)
                leaf_nodes.append(result)
            #print("LEAFNODES", leaf_nodes)
            unordered_parent_nodes = []
            for node in leaf_nodes:
                unordered_parent_nodes.append(ParentNode("li", node))
            #print(unordered_parent_nodes)
            convert_parent_node = ParentNode("ol", unordered_parent_nodes)
            html_nodes.append(convert_parent_node)
        if block_type == BlockType.QUOTE:
            split_lines = block.split("\n")
            stripped_lines = []
            for line in split_lines:
                #print("LINE", line)
                line = line[2:]
                #print("LINE", line)
                strip_space = line.strip()
                stripped_lines.append(strip_space)


            result = text_to_children(" ".join(stripped_lines))
            #print("QUOTE")
            #print(result)
            convert_parent_node = ParentNode("blockquote",result)
            #print(convert_parent_node)
            html_nodes.append(convert_parent_node)
        if block_type == BlockType.CODE:
#            print(block_type)
#            print(block)
#            print("RESULT")
            
            #for line in split_lines:
            #    if "```" in line:
            #        #print("FOUND")
             #       strip_code = line.strip("```")
             #       strip_newline = strip_code.strip()

            stripped =block[4:-3]

 #           print("".join(stripped))
            node = text_node_to_html_node(TextNode("".join(stripped), TextType.TEXT))      
            convert_parent_node = ParentNode("code",[node])
            again_parent_node = ParentNode("pre", [convert_parent_node])
            html_nodes.append(again_parent_node)



            
  #          print("CODE")
           # print(result)
           # convert_parent_node = ParentNode("code",result)
           # print("CPN===")
           # print(convert_parent_node)
            #print(convert_parent_node)
            #html_nodes.append(convert_parent_node)


            #print("UNORDERED")
            #print(result)
            #convert_parent_node = ParentNode("p",result)
            #print(convert_parent_node)
            #html_nodes.append(convert_parent_node)
        #    continue 

            #html_nodes.append(result)
        #if block_type == BlockType.UNORDERED_LIST:
        

        
   # print("HTML NODES", html_nodes)
    final_node = ""
    return ParentNode("div", html_nodes)
    #print(final_node)
    #return final_node.to_html()
    
    #for i in range(len(html_nodes), 1, -1):
        #print(i)
        #ParentNode(html_node[i])

    #count = 1
    #leafnode = len(formatted)
    #print("DICTIONARY")
    #print(formatted, "len", leafnode)
    #for item, key in formatted.items():
    #    print(item)
        # if heading
    #    html_nodes.append(ParentNode("h1",item))
    #    if count == leafnode:
    #        print("LeafNODE", item)
    #        html_nodes.append(LeafNode())

     #   count += 1

        #print("top")
        #print(block)
        #print(block_type)
        #if block_type == BlockType.PARAGRAPH:
        #    formatted[block] = BlockType.PARAGRAPH
        #    print("paragraph!!")
        #if block_type == BlockType.HEADING:
        #    print("HEADING")
        #    print(block)
        #    block_html = block.split("#")
        #    print("split")
        #    print(block_html)
        #    hn = HTMLNode("<h1>", block_html[1])
        #    formatted_nodes.append(ParentNode("h1", block_html[1].strip())) 
        
#paragraph types should get checked for bold and italics
   # identify blocks



def markdown_to_blocks(markdown):
    result =markdown.split("\n\n")
    result_list = []
    for block in result:
        stripped = block.strip()
        if block == "":
            continue
        result_list.append(stripped)

    return result_list

    

def block_to_block_type(block):
    heading = re.findall(r'(#{1,6} .*)', block)
    if heading:
        return BlockType.HEADING
    code_block = re.findall(r'```(.*?)```', block,  re.DOTALL)
    if code_block:
        return BlockType.CODE
    quote_block = re.findall(r'^(?:> ?.*\n?)+$', block)
    if quote_block:
        return BlockType.QUOTE
    unordered_block = re.findall(r'^(?:- .*(?:\n|$))+', block)
    if unordered_block:
        return BlockType.UNORDERED_LIST
    #ordered_block = re.findall(r'^(?:- .*(?:\n|$))+', block)
    num_start = "1"
    expected_start = f"{num_start}."
    ordered_block = re.findall(r'^(?:\d+\. .*(?:\n|$))+',block)
    #ordered_block.("\n")
    #print("block")
    #print(ordered_block[0])
    if ordered_block:
        for line in ordered_block:
           # print("start", expected_start)
           # print("line",line)
            if not line.startswith(f"{expected_start}"):
                print("not a valid sequence!")
                break
            expected_start = chr(ord(num_start) + 1)
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    #if ordered_block:
    #    return BlockType.UNORDED_LIST
    
#  with 1-6 # characters, followed by a space and then the heading text.
     
