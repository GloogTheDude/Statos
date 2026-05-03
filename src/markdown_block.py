from enum import Enum
from inline_markdown import *
from htmlnode import *
from textnode import *


class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDEREDLIST = "unordered_list",
    ORDEREDLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    returned =[]
    for i in range(len(blocks)):
        blocks[i]=blocks[i].strip()
        if len(blocks[i])>0:
            returned.append(blocks[i])
    for j in range(len(returned)):
        splitted=returned[j].split("\n")
        concat =""
        for s in splitted:
            s=s.strip()
            concat+=(s+"\n")
        returned[j]=concat.strip()
    return returned

def block_to_block_type(block:str):
    marks ={
            "headings_marks" : ("# ", "## ", "### ", "#### ", "##### ", "###### "),
            "multicode_marks": "```",
            "quote_mark": ">",
            "ul_mark": "- "
            #"ol_mark": "{i}."
    }

    if block.startswith(marks["headings_marks"]):
        return BlockType.HEADING
    lines = block.split("\n")
    if len(lines)>1:
        if lines[0].startswith(marks["multicode_marks"]) and lines[-1].startswith("```"):
            return BlockType.CODE
    isquote = True
    for l in lines: 
        if not l.startswith(marks["quote_mark"]):
            isquote=False
            break;
    if isquote:
        return BlockType.QUOTE
    isul=True
    for l in lines: 
        if not l.startswith(marks["ul_mark"]):
            isul =False
            break
    if isul: return BlockType.UNORDEREDLIST
    isol = True 
    i = 1
    for l in lines:
        if not l.startswith(f"{i}. "):
            isol= False
            break
        i+=1
    if isol: return BlockType.ORDEREDLIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    mark_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in mark_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_blocks.append(block_to_html_paragraph(block))
            case BlockType.HEADING:
                html_blocks.append(block_to_htlm_headings(block))
            case BlockType.CODE:
                html_blocks.append(block_to_html_codeblock(block))
            case BlockType.QUOTE:
                html_blocks.append(block_to_html_quote(block))
            case BlockType.UNORDEREDLIST:
                html_blocks.append(block_to_html_ul(block))
            case BlockType.ORDEREDLIST:
                html_blocks.append(block_to_html_ol(block))
            case _:
                raise Exception(" block_to_block_type(block) seems to fail to find a suitable BlockType")
    return ParentNode("div", html_blocks)

def block_to_html_paragraph(block):
    text = block.replace("\n"," ")
    return ParentNode("p",text_to_children(text))

def block_to_htlm_headings(block):
    lines = block.split(" ",1)
    tier = len(lines[0])
    return ParentNode(f"h{tier}", text_to_children(lines[1]))

def block_to_html_codeblock(block):
    block = block[3:-3].lstrip("\n")
    text_node = TextNode(block,TextType.TEXT)
    code_block = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code_block])

def block_to_html_quote(block):
    lines = block.split("\n")
    cleaned_lines = []
    for l in lines:
        cleaned_lines.append(l[1:].strip())
    cleaned_block = "\n".join(cleaned_lines)

    return ParentNode("blockquote", text_to_children(cleaned_block))

def block_to_html_ul(block):
    lines = block.split("\n")
    coll = []
    for l in lines:
        l = l.split("- ", 1)
        coll.append(ParentNode("li",text_to_children(l[1])))
    return ParentNode("ul", coll)

def block_to_html_ol(block):
    lines = block.split("\n")
    coll = []
    for l in lines:
        l = l.split(". ", 1)
        coll.append(ParentNode("li",text_to_children(l[1])))
    return ParentNode("ol", coll)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes =[]
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node)) 
    return html_nodes