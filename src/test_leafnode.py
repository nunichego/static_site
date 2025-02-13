import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_01(self):
        leaf1 = LeafNode("some text", None)
        result = "some text"
        self.assertEqual(leaf1.to_html(), result)

    def test_02(self):
        leaf2 = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf2.to_html(), result)

    def test_03(self):
        with self.assertRaises(ValueError):
            LeafNode(None, "p")

if __name__ == "__main__":
    unittest.main()