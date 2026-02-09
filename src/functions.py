import re
import os
import shutil

from leafnode import LeafNode
from textnode import TextNode, TextType
from blocktype import BlockType
from parentnode import ParentNode

#########################################################################
# Function: extract_markdown_images - extract alt and url from markdown #
#                                     which contains an image string    #
# Input:    text - markdown text                                        #
# Return:   tuple of matches (e.g. (alt, url))                          #
#########################################################################
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

##############################################################################
# Function: extract_markdown_links - extract link text and url from markdown #
#                                    which contains an link string           #
# Input:    text_node - markdown text                                        #
# Return:   tuple of matches (e.g. (link_text, link_url))                    #
##############################################################################
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

###############################################################
# Function: text_to_html_node - from TextNode create LeafNode #
# Input:    text_node - TextNode to convert                   #
# Return:   LeafNode                                          #
###############################################################
def text_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

        case _:
            raise Exception("Invalid text node type.")

##################################################################
# Function: split_nodes_delimiter - split TextNodes by delimiter #
# Input:    old_node  - list of old TextNodes                    #
#           delimiter - delimiter by which list is split         #
#           text_type - type of TextNode (matching delimiter)    #
# Return:   list of new splitted TextNodes                       #
##################################################################
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_nodes.append(node)
            continue

        # split nodes by delimiter
        seperate_values = node.text.split(delimiter)
        num_values = len(seperate_values)
        if (num_values % 2) == 0:
            raise SyntaxError("Invalid markdown syntax!")

        for i in range(num_values):
            if (i % 2) != 0:
                result_nodes.append(
                    TextNode(seperate_values[i], text_type)
                )
            else:
                result_nodes.append(
                    TextNode(seperate_values[i], TextType.PLAIN)
                )

    return result_nodes

##################################################################
# Function: split_nodes_images - split image TextNode into nodes #
#                                for text and image              #
# Input:    old_node  - list of old TextNodes                    #
# Return:   list of new splitted TextNodes for image             #
##################################################################
def split_nodes_images(old_nodes):
    result_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_nodes.append(node)
            continue

        orgiginal_text = node.text
        img_matches = extract_markdown_images(orgiginal_text)

        for alt, url in img_matches:
            sections = orgiginal_text.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                result_nodes.append(
                    TextNode(sections[0], TextType.PLAIN)
                )

            result_nodes.append(TextNode(alt, TextType.IMAGE, url))

            orgiginal_text = sections[1]

        if orgiginal_text != "":
            result_nodes.append(TextNode(orgiginal_text, TextType.PLAIN))

    return result_nodes

##################################################################
# Function: split_nodes_links - split link TextNode into nodes   #
#                                for text and link               #
# Input:    old_node  - list of old TextNodes                    #
# Return:   list of new splitted TextNodes for links             #
##################################################################
def split_nodes_links(old_nodes):
    result_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_nodes.append(node)
            continue

        orgiginal_text = node.text
        img_matches = extract_markdown_links(orgiginal_text)

        for alt, url in img_matches:
            sections = orgiginal_text.split(f"[{alt}]({url})", 1)
            if sections[0] != "":
                result_nodes.append(
                    TextNode(sections[0], TextType.PLAIN)
                )

            result_nodes.append(TextNode(alt, TextType.LINK, url))

            orgiginal_text = sections[1]

        if orgiginal_text != "":
            result_nodes.append(TextNode(orgiginal_text, TextType.PLAIN))

    return result_nodes

#############################################################################
# Function: text_to_textnodes - converts text into list of textnodes        #
#                               depending on delimiter / type (image, link) #
# Input:    text - text to convert                                          #
# Return:   list of TextNodes after splitting                               #
#############################################################################
def text_to_textnodes(text):
    result_nodes = [TextNode(text, TextType.PLAIN)]

    result_nodes = (split_nodes_delimiter(result_nodes, '**', TextType.BOLD))
    result_nodes = (split_nodes_delimiter(result_nodes, '_', TextType.ITALIC))
    result_nodes = (split_nodes_delimiter(result_nodes, '`', TextType.CODE))
    result_nodes = (split_nodes_images(result_nodes))
    result_nodes = (split_nodes_links(result_nodes))

    return result_nodes

###################################################################
# Function: markdown_to_blocks - converts single markdown string  #
#                                into list of markdown blocks     #
#                                (split by newlines)              #
# Input:    markdown - markdown string                            #
# Return:   list of markdown blocks (strings splitted by newline) #
###################################################################
def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split("\n\n")
    for line in lines:
        if line == "":
            continue

        blocks.append(line.strip())
    return blocks

######################################################################
# Function: block_to_block_type - get block type from markdown block #
# Input:    markdown - markdown block                                #
# Return:   BlockType of markdown block                              #
######################################################################
def block_to_block_type(markdown):
    b_type = BlockType.PARAGRAPH

    # headings
    if markdown.startswith('#'):
        count = 0
        for i in range(len(markdown)):
            if markdown[i] == ' ':
                break

            if count >= 6:
                break

            if markdown[i] == '#':
                count += 1
                continue

            break

        if count < len(markdown) and count >= 1 and count <=6:
            if markdown[count] == ' ':
                return BlockType.HEADING

        return BlockType.PARAGRAPH

    # code blocks
    if markdown.startswith('```\n') and markdown.endswith('```'):
        return BlockType.CODE

    # quotes
    if markdown.startswith('>'):
        return BlockType.QUOTE

    # unordered list
    if markdown.startswith('- '):
        list_entries = markdown.split('\n')
        is_valid_ulist = True
        for entry in list_entries:
            if not entry.startswith('- '):
                is_valid_ulist = False
                break

        return BlockType.UNORDERED_LIST if is_valid_ulist else BlockType.PARAGRAPH

    # ordered list
    if markdown.startswith('1. '):
        list_entries = markdown.split('\n')
        is_valid_olist = True
        for i in range(len(list_entries)):
            if not list_entries[i].startswith(f"{i+1}. "):
                is_valid_olist = False

        return BlockType.ORDERED_LIST if is_valid_olist else BlockType.PARAGRAPH

    return b_type


########################################################################
# Function: text_to_children - converts markdown text to html children #
# Input:    text - text to convert                                     #
# Return:   list of html children                                      #
########################################################################
def text_to_children(text):
    html_children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_children.append(text_to_html_node(text_node))
    return html_children

########################################################################
# Function: prepare_heading_block - trim block from # symbols and      #
#                                   and count level of heading         #
# Input:    block - text of block                                      #
# Return:   trimmed block text                                         #
#           level of heading                                           #
########################################################################
def prepare_heading_block(block):
    trimmed = ""
    level = 0

    # count consecutive hashtag characters at the beginning of the block text
    for i in range(len(block)):
        if block[i] == ' ':
            break
        if level >= 6:
            break
        if block[i] == '#':
            level += 1

    if level >= len(block) or level < 1 or level > 6:
        raise ValueError("Invalid markdown heading!")

    trimmed = block[level+1:]
    return trimmed, level

########################################################################
# Function: prepare_quote_block - remove markdown quote character and  #
#                                 whitespaces from quotes              #
# Input:    block - text of block                                      #
# Return:   trimmed block text                                         #
########################################################################
def prepare_quote_block(block):
    lines = block.split('\n')
    result = []
    for line in lines:
        result.append(line[1:].strip())
    return '\n'.join(result)

#############################################################################
# Function: prepare_unordered_list_block - get all list children for block  #
# Input:    block - text of block                                           #
# Return:   list of list childrens                                          #
#############################################################################
def prepare_unordered_list_block(block):
    lines = block.split('\n')
    li_children = []
    for line in lines:
        text = line[2:].strip()
        elem_children = text_to_children(text)
        li_children.append(ParentNode("li", elem_children))
    return li_children

#############################################################################
# Function: prepare_ordered_list_block - get all list children for block    #
# Input:    block - text of block                                           #
# Return:   list of list childrens                                          #
#############################################################################
def prepare_ordered_list_block(block):
    lines = block.split('\n')
    li_children = []
    for i, line in enumerate(lines):
        prefix_len = len(f"{i+1}. ")
        elem_children = text_to_children(line[prefix_len:])
        li_children.append(ParentNode("li", elem_children))
    return li_children


####################################################################
# Function: block_to_html - converts markdown block into html node #
# Input:    block      - markdown block                            #
#           block_type - type of markdown block                    #
# Return:   HTMLNode                                               #
####################################################################
def block_to_html(block, block_type):
    match (block_type):
        case BlockType.PARAGRAPH:
            lines = block.split('\n')
            text = " ".join(line.strip() for line in lines if line.strip() != "")
            return ParentNode("p", text_to_children(text))

        case BlockType.HEADING:
            text, level = prepare_heading_block(block)
            return ParentNode(f"h{level}", text_to_children(text))

        case BlockType.QUOTE:
            text = prepare_quote_block(block)
            return ParentNode("blockquote", text_to_children(text))

        case BlockType.UNORDERED_LIST:
            children = prepare_unordered_list_block(block)
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            children = prepare_ordered_list_block(block)
            return ParentNode("ol", children)

        case BlockType.CODE:
            lines = block.split('\n')
            text = '\n'.join(lines[1:-1]) + '\n'
            text_node = TextNode(text, TextType.CODE)
            code_html_node = text_to_html_node(text_node)
            return ParentNode("pre", [ code_html_node ])

        case _:
            raise ValueError("Invalid block type!")

###################################################################
# Function: markdown_to_html_node - converts markdown string into #
#                                   html nodes with children      #
# Input:    markdown - markdown string to convert                 #
# Return:   HTMLNode with children                                #
###################################################################
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    html_children = []
    outer_parent = ParentNode("div", html_children)

    for block in blocks:
        b_type = block_to_block_type(block)
        html_node = block_to_html(block, b_type)
        html_children.append(html_node)

    return outer_parent

###################################################################
# Function: extract_title - extract title from markdown string    #
# Input:    markdown - markdown string                            #
# Return:   title text                                            #
###################################################################
def extract_title(markdown):
    lines = markdown.split('\n')
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
            break

    if title == "":
        raise ValueError("Invalid markdown, no title heading!")

    return title

###################################################################
# Function: copy_dir - copies contents from source directory into #
#                      destination directory                      #
# Input:    src  - source directory                               #
#           dest - destination directory                          #
# Return:                                                         #
###################################################################
def copy_dir(src, dest):
    src_path = os.path.abspath(src)
    dest_path = os.path.abspath(dest)

    print("Current working dir:", os.getcwd())
    print("Src path:", src_path)
    if not os.path.exists(src_path) or not os.path.isdir(src_path):
        raise ValueError("Invalid path for src directory")

    print("Dest path:", dest_path)
    if not os.path.exists(dest_path) or not os.path.isdir(dest_path):
        raise ValueError("Invalid path for dest directory")

    # first delete dest directory and recreate it
    print("Clearing destination directory...")
    shutil.rmtree(dest_path)
    os.mkdir(dest_path)

    # get files and directories from source
    src_contents = os.listdir(src_path)

    for content in src_contents:
        src_sub_path = os.path.join(src_path, content)
        if os.path.isfile(src_sub_path):
            # just copy files into dest dir as is
            print("Copy file \"", src_sub_path, "\" to \"", dest_path, "\"")
            shutil.copy(src_sub_path, dest_path)
        else:
            # create new directory in destination and recursivly call copy on that dir
            dest_sub_path = os.path.join(dest_path, content)
            os.mkdir(dest_sub_path)
            print("Copy directory \"", src_sub_path, "\" to directory \"", dest_sub_path, "\"")
            copy_dir(src_sub_path, dest_sub_path)

##########################################################################
# Function: generate_page -  generate html page from markdown file       #
# Input:    from_path     - source path                                  #
#           template_path - template path                                #
#           dest_path     - dest path                                    #
#           basepath         - path to the root directory of the project #
# Return:                                                                #
##########################################################################
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    src = os.path.abspath(from_path)
    dest = os.path.abspath(dest_path)
    template = os.path.abspath(template_path)

    with open(src) as f:
        markdown = f.read()

    with open(template) as f:
        html_template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_title = extract_title(markdown)
    html_body = html_node.to_html()

    html_content = html_template.replace("{{ Title }}", html_title)
    html_content = html_content.replace("{{ Content }}", html_body)

    html_content = html_content.replace("href=\"\/", f"href=\"{basepath}")
    html_content = html_content.replace("src=\"\/", f"src=\"{basepath}")

    dir_name = os.path.dirname(dest)
    os.makedirs(dir_name, exist_ok=True)
    with open(dest, "w") as f:
        f.write(html_content)

##########################################################################
# Function: generate_pages_recursive - generate html from nested         #
#                                      markdown directories              #
# Input:    dir_path_content - directory with children to generate from  #
#           template_path    - template path                             #
#           dest_dir_path    - destination directory to generate to      #
#           basepath         - path to the root directory of the project #
# Return:                                                                #
##########################################################################
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_path = os.path.abspath(dir_path_content)
    dest_path = os.path.abspath(dest_dir_path)

    contents = os.listdir(content_path)
    for content in contents:
        sub_path = os.path.join(content_path, content)
        dest_sub_path = os.path.join(dest_path, content)
        if os.path.isfile(sub_path):
            # handle file case
            if content.endswith(".md"):
                generate_page(sub_path, template_path, dest_sub_path.replace(".md", ".html"), basepath)
        else:
            generate_pages_recursive(sub_path, template_path, dest_sub_path, basepath)