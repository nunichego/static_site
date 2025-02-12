import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_1(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_eq_2(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_testcase"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_testcase"')

    def test_eq_3(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_testcase", "some": None})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_testcase" some="None"')

    def test_eq_4(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()