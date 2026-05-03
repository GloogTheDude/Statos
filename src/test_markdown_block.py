import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown_block import *


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks_basic(self):
        md = """# This is a heading

            This is a paragraph of text.

            - Item 1
            - Item 2"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_markdown_to_blocks_removes_extra_spaces(self):
        md = """This is text
        This is indented

        - item one
        - item two"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is text\nThis is indented",
                "- item one\n- item two",
            ],
        )

    def test_markdown_to_blocks_ignores_empty_blocks(self):
        md = """

Paragraph one



Paragraph two

"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Paragraph one",
                "Paragraph two",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING,
        )

    def test_code_block(self):
        block = """```
print("hello")
```"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_quote_block(self):
        block = """> quote line one
> quote line two"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        block = """- item one
- item two
- item three"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDEREDLIST,
        )

    def test_ordered_list(self):
        block = """1. item one
2. item two
3. item three"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDEREDLIST,
        )

    def test_invalid_ordered_list_becomes_paragraph(self):
        block = """1. item one
3. item three"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        block = "This is just a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_mixed_quote_becomes_paragraph(self):
        block = """> quote line
normal line"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_mixed_unordered_list_becomes_paragraph(self):
        block = """- item one
not an item"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    """=================================="""

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    

    """=========================="""


    def test_heading_h1(self):
        md = """
    # This is a heading
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>",
        )


    def test_heading_h3(self):
        md = """
    ### This is a level 3 heading
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h3>This is a level 3 heading</h3></div>",
        )


    def test_quote_single_line(self):
        md = """
    > This is a quote
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>",
        )


    def test_quote_multiple_lines(self):
        md = """
    > This is a quote
    > split on two lines
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nsplit on two lines</blockquote></div>",
        )


    def test_unordered_list(self):
        md = """
    - First item
    - Second item
    - Third item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )


    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item
    3. Third item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )


    def test_multiple_block_types(self):
        md = """
    # Title

    This is a paragraph with **bold** text.

    - Item one
    - Item two

    > This is quoted
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>Item one</li><li>Item two</li></ul><blockquote>This is quoted</blockquote></div>",
        )


    def test_paragraph_with_link(self):
        md = """
    This is a paragraph with a [link](https://example.com).
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://example.com">link</a>.</p></div>',
        )


    def test_paragraph_with_image(self):
        md = """
    This is a paragraph with an ![image](https://example.com/image.png).
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected= '<div><p>This is a paragraph with an <img src="https://example.com/image.png" alt="image"></img>.</p></div>'
        with open("results.txt", "w") as f:
            f.write(node.to_html())
            f.write("\n")
            f.write(expected)

        self.assertEqual(
            html,
            expected
        )


    def test_list_items_with_inline_markdown(self):
        md = """
    - This has **bold**
    - This has _italic_
    - This has `code`
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>This has <b>bold</b></li><li>This has <i>italic</i></li><li>This has <code>code</code></li></ul></div>",
        )


    def test_ordered_list_wrong_numbering_becomes_paragraph(self):
        md = """
    1. First item
    3. Third item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>1. First item 3. Third item</p></div>",
        )

if __name__ == "__main__":
    unittest.main()