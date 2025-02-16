import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    def single_node_split(node, delimiter, text_type):
        if not isinstance(node, TextNode):
            raise Exception("input element is not a TextNode")
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid Markdown syntax")

        nodes_list = [(
            TextNode(text, TextType.TEXT)) for text in node.text.split(delimiter)]

        for node in nodes_list[1::2]:
            node.text_type = text_type

        return [node for node in nodes_list if node.text != ""]
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_result = single_node_split(node, delimiter, text_type)
            new_nodes.extend(split_result)
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(((?:[^\(\)]|\([^\(\)]*\))*)\)", text)

def single_item_node_split(node, text_type=TextType.LINK):
    if not isinstance(node, TextNode):
        raise Exception("input element is not a TextNode")
    
    link_image_definer = ""
    if text_type == TextType.IMAGE:
        link_image_definer = "!"
    func = extract_markdown_links if text_type == TextType.LINK else extract_markdown_images

    extracted_tuples = func(node.text)
    if not extracted_tuples:
        return [node]
    
    delimiters = []
    valid_tuples = []

    for tuple in extracted_tuples:
        if text_type == TextType.LINK and not tuple[1].strip():
            continue
        valid_tuples.append(tuple)
        combined_value = f"{link_image_definer}[{tuple[0]}]({tuple[1]})"
        delimiters.append(combined_value)

    if not valid_tuples:
        return [node]

    result_list = []
    regex_pattern = "|".join(map(re.escape, delimiters))
    text_elements = re.split(regex_pattern, node.text)

    for i in range (0, len(text_elements)):
        if text_elements[i]:
            result_list.append(TextNode(text_elements[i], TextType.TEXT))
        if i < len(valid_tuples):
            result_list.append(TextNode(valid_tuples[i][0], text_type, valid_tuples[i][1]))
    
    return result_list

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_result = single_item_node_split(node, TextType.IMAGE)
            new_nodes.extend(split_result)
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_result = single_item_node_split(node)
            new_nodes.extend(split_result)
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)], 
                        "**", TextType.BOLD), 
                        "*", TextType.ITALIC), 
                        "`", TextType.CODE)))