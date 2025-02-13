import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):

    def test_creation(self):
        parent1 = ParentNode("div", [LeafNode(
            "p", "some text")], {"class": "container", "id": "main"})
        test_parent = "HTMLNode(div, None, " \
            "[HTMLNode(some text, p, None, None)], " \
            "{'class': 'container', 'id': 'main'})"
        self.assertEqual(str(parent1), test_parent)

    def test_to_html_01(self):
        parent1 = ParentNode("div", [LeafNode(
            "some text", "p")], {"class": "container", "id": "main"})
        result = '<div class="container" id="main"><p>some text</p></div>'
        self.assertEqual(parent1.to_html(), result)

    def test_ValueError(self):
        with self.assertRaises(ValueError):
            ParentNode("", None)



if __name__ == "__main__":
    unittest.main()