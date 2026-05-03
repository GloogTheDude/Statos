from textnode import TextNode, TextType
from htmlnode import *
import re

from enum import Enum



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for on in old_nodes:
        if on.text_type != TextType.TEXT:
            new_nodes.append(on)
        else:
            splitted = on.text.split(delimiter)
            if len(splitted) % 2 ==0:
                raise Exception("invalid Markdown syntax")
            else:
                for i in range(len(splitted)):
                    if splitted[i] == "":
                        continue
                    if i % 2 ==0:
                        new_nodes.append(TextNode(splitted[i],TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(splitted[i],text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for on in old_nodes:
        if on.text_type != TextType.TEXT:
            new_nodes.append(on)
            continue
        extracted = extract_markdown_images(on.text)
        if len(extracted) == 0:
            new_nodes.append(on)
        else:
            match=extracted
            #print(f"match = {match}")
            text = on.text
            for m in match:
                #print(f"text = {text}")
                #print(f"m = {m}")
                split_strings = text.split(f"![{m[0]}]({m[1]})",1)
                #print(f"split_strings = {split_strings}")
                if len(split_strings[0])>0:
                    new_nodes.append(TextNode(split_strings[0], TextType.TEXT))
                new_nodes.append(TextNode(m[0],TextType.IMAGES,m[1]))
                text = split_strings[1]
            if len(text) > 0: new_nodes.append(TextNode(text, TextType.TEXT))
    #print(f"new_nodes={new_nodes}")
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for on in old_nodes:
        if on.text_type != TextType.TEXT:
            new_nodes.append(on)
            continue
        extracted = extract_markdown_links(on.text)
        if len(extracted) == 0:
            new_nodes.append(on)
        else:
            match=extracted
            #print(f"match = {match}")
            text = on.text
            for m in match:
                #print(f"text = {text}")
                #print(f"m = {m}")
                split_strings = text.split(f"[{m[0]}]({m[1]})",1)
                #print(f"split_strings = {split_strings}")
                if len(split_strings[0])>0:
                    new_nodes.append(TextNode(split_strings[0], TextType.TEXT))
                new_nodes.append(TextNode(m[0],TextType.LINKS,m[1]))
                text = split_strings[1]
            if len(text) > 0 : new_nodes.append(TextNode(text, TextType.TEXT))
    #print(f"new_nodes={new_nodes}")
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes =split_nodes_delimiter(nodes,'**', TextType.BOLD)
    nodes =split_nodes_delimiter(nodes,"`", TextType.CODE)
    nodes =split_nodes_delimiter(nodes,'_', TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

