from copy import deepcopy
from logging import root

import html5lib

from html_mutation.html import dom


# def test_bs4_copy():
#     dom_text = """
#     <html>
#         <body>
#             <h1>Hello</h2>
#             <p><span>This is a DOM</span></p>
#         </body>
#     </html>"""
#     root = html5lib.parse(dom_text, treebuilder="lxml").getroot()
#     dom_copy = root.__copy__()
#     deepcopy_dom = deepcopy(dom)
#     assert deepcopy_dom == dom_copy


def test_change_node():
    dom_text = """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
    tree = html5lib.parse(dom_text, treebuilder="lxml")
    child = dom.find_all(tree, 'p')[0]
    assert '{http://www.w3.org/1999/xhtml}p' == child.tag


def test_xpath():
    dom_text = """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
    tree = html5lib.parse(dom_text, treebuilder="lxml")
    child = dom.find_all(tree, 'p')[0]
    assert '/html/body/p' == dom.get_xpath(tree, child)
