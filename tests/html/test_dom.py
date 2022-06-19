from html_mutation.html import dom
from html_mutation.html.tags import Tag


def test_find_by_xpath():
    tree = dom.parse(get_simple_dom())
    target = tree.find_by_xpath("/html/body/p")[0]
    assert 1 == len(target)
    assert "p" == target.tag


def test_find_all_one_tag():
    tree = dom.parse(get_simple_dom())
    target = tree.find_by_tag(Tag.P)[0]
    assert 1 == len(target)
    assert "p" == target.tag


def test_find_all_multiple_tags():
    tree = dom.parse(get_simple_dom())
    target = tree.find_by_tag([Tag.P, Tag.H1])
    assert 2 == len(target)


def test_get_xpath():
    tree = dom.parse(get_simple_dom())
    child = tree.find_by_tag(Tag.P)[0]
    assert "/html/body/p" == tree.get_xpath(child)


def get_simple_dom():
    return """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
