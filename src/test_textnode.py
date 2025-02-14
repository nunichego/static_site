import unittest

from textnode import *
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a test node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://test.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.BOLD, "")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_textnode_to_LeafNode_01(self):
        node = TextNode("some text", TextType.TEXT)
        leafnode = LeafNode("some text", None)
        self.assertEqual(text_node_to_html_node(node), leafnode)

    def test_textnode_to_LeafNode_02(self):
        node = TextNode("some text", TextType.BOLD)
        leafnode = LeafNode("some text", "b")
        self.assertEqual(text_node_to_html_node(node), leafnode)

    def test_normal_text(self):
        tn = TextNode("Hello", TextType.TEXT)
        expected = LeafNode("Hello", None)
        result = text_node_to_html_node(tn)
        self.assertEqual(result, expected)

    def test_bold_text(self):
        tn = TextNode("Bold", TextType.BOLD)
        expected = LeafNode("Bold", "b")
        result = text_node_to_html_node(tn)
        self.assertEqual(result, expected)

    def test_italic_text(self):
        tn = TextNode("Italic", TextType.ITALIC)
        expected = LeafNode("Italic", "i")
        result = text_node_to_html_node(tn)
        self.assertEqual(result, expected)

    def test_code_text(self):
        tn = TextNode("print('Hello')", TextType.CODE)
        expected = LeafNode("print('Hello')", "code")
        result = text_node_to_html_node(tn)
        self.assertEqual(result, expected)

    def test_link_text(self):
        tn = TextNode("Example", TextType.LINK, url="http://example.com")
        expected = LeafNode("Example", "a", {"href": "http://example.com"})
        result = text_node_to_html_node(tn)
        self.assertEqual(result, expected)

    def test_image_text(self):
        tn = TextNode("Image alt text", TextType.IMAGE, url="http://example.com/image.png")
        expected = LeafNode("", "img", {"src": "http://example.com/image.png", "alt": "Image alt text"})
        result = text_node_to_html_node(tn)
        self.assertEqual(result, expected)

    def test_invalid_text_type(self):
        # Create a dummy enum to simulate an invalid text type.
        class DummyTextType(Enum):
            UNKNOWN = "unknown"

        tn = TextNode("Invalid", DummyTextType.UNKNOWN)
        with self.assertRaises(Exception):
            text_node_to_html_node(tn)
        


if __name__ == "__main__":
    unittest.main()