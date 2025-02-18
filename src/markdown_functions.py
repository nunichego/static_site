import re
from textnode import *
from htmlnode import *

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

def markdown_to_blocks(markdown):
    result_strings = markdown.split("\n\n")
    result_strings = [string for string in result_strings if string != ""]
    return list(map(lambda x: x.strip(), result_strings))

def block_to_block_type(block):

    possible_headings = tuple(["#" * i + " " for i in range(1, 7)])
    lines = block.split("\n")

    if block.startswith(possible_headings):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in lines):
        return "quote"
    elif all((line.startswith("* ") or line.startswith("- ")) for line in lines):
        return "unordered_list"
    elif all(line.startswith(f"{(lines.index(line) + 1)}. ") for line in lines):
        return "ordered_list"
    else:
        return "paragraph"

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        if block_type == "heading":
            children.append(create_heading_node(block))
        elif block_type == "code":
            children.append(create_code_node(block))
        elif block_type == "quote":
            children.append(create_quote_node(block))
        elif block_type == "unordered_list":
            children.append(create_unordered_list_node(block))
        elif block_type == "ordered_list":
            children.append(create_ordered_list_node(block))
        elif block_type == "paragraph":
            children.append(create_paragraph(block))
        else:
            raise Exception("unknown Error")     
    return ParentNode("div", children)

def create_heading_node(block):
    heading_level = 1
    current_prefix = ""
    for index, prefix in enumerate(tuple(["#" * i for i in range(1, 7)])):
        if block.startswith(prefix):
            heading_level = index + 1
            current_prefix = f"{prefix} "
    return ParentNode(f"h{heading_level}", text_to_children(block.removeprefix(current_prefix).split("\n")[0]))

def create_unordered_list_node(block):
    children = []
    for line in block.split("\n"):
        clean_line = line.removeprefix("* ").removeprefix("- ").removeprefix("+ ")
        children.append(ParentNode("li", text_to_children(clean_line)))
    return ParentNode("ul", children)

def create_quote_node(block):
    clean_block = "\n".join([line.removeprefix(">").strip() for line in block.split("\n")])
    children = text_to_children(clean_block)
    return ParentNode("blockquote", children)

def create_ordered_list_node(block):
    children = []
    for line in block.split("\n"):
        clean_line = line[line.find(". ") + 2:]
        children.append(ParentNode("li", text_to_children(clean_line)))
    return ParentNode("ol", children)

def create_paragraph(block):
    return (ParentNode("p", text_to_children(block)))

def create_code_node(block):
    clean_block = block.strip("```")
    children = text_to_children(clean_block)
    return ParentNode("pre", [ParentNode("code", children)])

def text_to_children(text_line):
    children = []
    for node in text_to_textnodes(text_line):
        children.append(text_node_to_html_node(node))
    return children

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            return line.strip().strip("# ").strip()
    raise Exception("no title found")

