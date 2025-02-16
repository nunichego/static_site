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
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = (extract_markdown_images(text))
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)


    def test_extracting_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = (extract_markdown_links(text))
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()