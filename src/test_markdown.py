import unittest
from markdown_functions import *
from textnode import TextNode, TextType

class TestDelimiter(unittest.TestCase):

    def test_basic_bold_text(self):
        nodes1 = [TextNode("This is **bold** text", TextType.TEXT)]
        result1 = split_nodes_delimiter(nodes1, "**", TextType.BOLD)
        expected = "[TextNode(This is , text, None), "\
            "TextNode(bold, bold, None), "\
                "TextNode( text, text, None)]"
        self.assertEqual(str(result1), expected)

    def test_multiple_bold_sections(self):
        nodes2 = [TextNode("Start **bold** middle **bold** end", TextType.TEXT)]
        result2 = split_nodes_delimiter(nodes2, "**", TextType.BOLD)
        expected = "[TextNode(Start , text, None), "\
            "TextNode(bold, bold, None), TextNode( middle , text, None), "\
                "TextNode(bold, bold, None), TextNode( end, text, None)]"
        self.assertEqual(str(result2), expected)

    def test_mix_of_different_nodes(self):
        nodes3 = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("more **bold** text", TextType.TEXT)
        ]
        result3 = split_nodes_delimiter(nodes3, "**", TextType.BOLD)
        nodes_result_expected = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result3, nodes_result_expected)

    def test_extracting_images(self):
        text = "This is text with a ![rick roll]"\
            "(https://i.imgur.com/aKaOqIh.gif) and "\
                "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = (extract_markdown_images(text))
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)


    def test_extracting_links(self):
        text = "This is text with a link [to boot dev]"\
            "(https://www.boot.dev) and [to youtube]"\
                "(https://www.youtube.com/@bootdotdev)"
        result = (extract_markdown_links(text))
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)

    def test_split_nodes_image_01(self):

        text1 = "Markdown makes it easy to include links in your text. For example, if you want to learn more about Markdown itself, "
        text2 = "check out the [Markdown Guide](https://www.markdownguide.org). You can also explore popular resources like [GitHub](https://github.com)"
        text3 = "for code hosting and collaboration.\n\nIf you're looking for tutorials, [freeCodeCamp](https://www.freecodecamp.org)"
        text4 = "offers extensive lessons on web development. Additionally, for daily tech news and insights, visit [TechCrunch](https://techcrunch.com)"

        test_nodes = [
            TextNode(text1, TextType.TEXT),
            TextNode(text2, TextType.TEXT)
            #TextNode(text3, TextType.TEXT),
            #TextNode(text4, TextType.TEXT),
        ]

        result = split_nodes_link(test_nodes)
        expected = [
            TextNode(text1, TextType.TEXT),
            TextNode("check out the ", TextType.TEXT),
            TextNode("Markdown Guide", TextType.LINK, "https://www.markdownguide.org"),
            TextNode(". You can also explore popular resources like ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com")
        ]
        print()
        self.assertEqual(result, expected)

    def test_split_nodes_links_image_02(self):

        text1 = "Here's a [link with (parentheses)](http://example.com/page(1))"
        text2 = "Same [link](url) twice [link](url)"
        text3 = "Empty alt text ![](image.jpg) or empty URL [text]()"

        test_nodes = [
            TextNode(text1, TextType.TEXT),
            TextNode(text2, TextType.TEXT),
            TextNode(text3, TextType.TEXT)
        ]

        result = split_nodes_link(split_nodes_image(test_nodes))
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("link with (parentheses)", TextType.LINK, "http://example.com/page(1)"),
            TextNode("Same ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" twice ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("Empty alt text ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "image.jpg"),
            TextNode(" or empty URL [text]()", TextType.TEXT)

            
        ]
        self.assertEqual(result, expected)

    def test_to_textnodes_01(self):
        text_example = "This is **text** with an *italic* word "\
            "and a `code block` and an ![obi wan image]"\
                "(https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text_example)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_markd_to_blocks(self):
        markd_examp = " # This is a heading\n\nThis is a paragraph "\
            "of text. It has some **bold** and *italic* words inside of"\
                " it. \n\n* This is the first list item in a list block\n* "\
                    "This is a list item\n* This is another list item"
        expected = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(markdown_to_blocks(markd_examp), expected)

    def test_block_to_type_01(self):
        block_ex = "1. - >```### Wow, \n2. * >really!\n3. 4445"
        self.assertEqual(block_to_block_type(block_ex), "ordered_list")

if __name__ == "__main__":
    unittest.main()