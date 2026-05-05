from textnode import TextType, TextNode 
import re






def markdown_to_blocks(markdown):
    result =markdown.split("\n\n")
    result_list = []
    for block in result:
        stripped = block.strip()
        if block == "":
            continue
        result_list.append(stripped)

    return result_list



def text_to_textnodes(text):    
    full_list = []

    nodes = [TextNode(text, TextType.TEXT)]
    #print(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    #print(nodes)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    #print(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_images(text):
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    #print(matches)
    return matches
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

def extract_markdown_links(text):
    matches = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []

    for node in old_nodes:
        #print(node)
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        extract = extract_markdown_images(node.text)
        if len(extract) == 0:
            new_list.append(node)
            continue
       # print(extract)
        
        text = node.text
        to_save = []
        for image in extract:
            section = text.split(f"![{image[0]}]({image[1]})", 1)
            text_again = TextNode(section[0], TextType.TEXT)
            text_image = (TextNode(image[0], TextType.IMAGE, image[1]))
            if text_again.text != "":
                to_save.append(text_again)
            if text_image.text != "":
                to_save.append(text_image)
            text = section[1]
        if text != "":
            to_save.append(TextNode(text, TextType.TEXT))
        new_list.extend(to_save)
    return new_list

def split_nodes_link(old_nodes): 
    new_list = []

    for node in old_nodes:
        #print(node)
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        extract = extract_markdown_links(node.text)
        if len(extract) == 0:
            new_list.append(node)
            continue
        #print(extract)
        text = node.text
        to_save = []
        for link in extract:
            section = text.split(f"[{link[0]}]({link[1]})", 1)
            text_again = TextNode(section[0], TextType.TEXT)
            text_image = (TextNode(link[0], TextType.LINK, link[1]))

            if text_again.text != "":
                to_save.append(text_again)
            if text_image.text != "":
                to_save.append(text_image)

            text = section[1]

        if text != "":
            to_save.append(TextNode(text, TextType.TEXT))
        new_list.extend(to_save)
    return new_list
   


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_list = []

    for node in old_nodes:
        split_list = []
        #print(node)
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        #print("nt", node.text)
        #print("deimiter", delimiter)
        
            #print(node.text.split(delimiter))
        split = node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        list_2 = []
        for i in range(len(split)):
            if split[i] == "":
                continue
            if i % 2 == 0:
                list_2.append(TextNode(split[i], TextType.TEXT))
            
            else:
                list_2.append(TextNode(split[i], text_type))

        new_list.extend(list_2)
    #print("NEW LIST", new_list)
    return new_list


