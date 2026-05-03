import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2, "test_eq NOK")
    
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD,"an url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2, "test_url NOK")

    def test_otherurl(self):
        node = TextNode("This is a text node", TextType.BOLD,"an url")
        node2 = TextNode("This is a text node", TextType.BOLD,"another url")
        self.assertNotEqual(node, node2, "test_otherurl NOK")
    
    def test_type(self):
        node = TextNode("This is a text node", TextType.LINKS)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2, "test_type NOK")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
if __name__ == "__main__":
    unittest.main()
