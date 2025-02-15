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