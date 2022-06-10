from copy import deepcopy

from bs4 import BeautifulSoup

from html_mutation.html.dom import xpath


def test_bs4_copy():
    dom_text = """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
    dom = BeautifulSoup(dom_text, "html5lib")
    dom_copy = dom.__copy__()
    deepcopy_dom = deepcopy(dom)
    assert dom == deepcopy_dom == dom_copy


def test_change_node():
    dom_text = """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
    dom = BeautifulSoup(dom_text, "html5lib")
    child = dom.find_all("p")[0]
    savedElement = child
    print("\n")
    print(dom)
    child.string = child.string + child.string
    print("\n")
    print(dom)
    child = savedElement
    print("\n")
    print(dom)


def test_xpath():
    dom_text = """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
    dom = BeautifulSoup(dom_text, "html5lib")
    child = dom.find_all("p")[0]
    print(xpath(child))
