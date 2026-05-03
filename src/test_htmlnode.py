import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="a",value="youtube.com")
        self.assertEqual(node, node2)
    
    def test_tag(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="b",value="youtube.com")
        self.assertNotEqual(node, node2)
    
    def test_value(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="a",value="1youtube.com")
        self.assertNotEqual(node, node2)
    
    def test_children(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="a",value="1youtube.com")
        node3 = HTMLNode(tag="p", value="hello world")
        children = []
        children.append(node3)
        node.children = children
        self.assertNotEqual(node, node2)
    
    def test_eq_children(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="a",value="youtube.com")
        node3 = HTMLNode(tag="p", value="hello world")
        children = []
        children.append(node3)
        node.children = children
        node2.children = children
        self.assertEqual(node, node2)

    def test_props(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="a",value="youtube.com")
        props = {"href":"youtube.com", "color": "red"}
        node.props = props
        self.assertNotEqual(node, node2)
    
    def test_eq_props(self):
        node = HTMLNode(tag="a",value="youtube.com")
        node2 = HTMLNode(tag="a",value="youtube.com")
        props = {"href":"youtube.com", "color": "red"}
        node.props = props
        node2.props = props
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="a",value="youtube.com")
        props = {"href":"https://www.google.com", "target": "_blank"}
        node.props = props
        attended_result=  ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), attended_result)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_noTag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_leaf_to_html_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )