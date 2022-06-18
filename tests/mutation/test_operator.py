from xml.etree import ElementTree
from html_mutation.html.dom import parse
from html_mutation.html.tags import Tag
from html_mutation.mutation import operator


def test_constructor_none():
    op = operator.ChangeTextOperator()
    assert len(op.tags) == 10


def test_contructor_ignore():
    op = operator.ChangeTextOperator(set([Tag.A, Tag.H6]))
    assert len(op.tags) == 8


def test_tc_muate():
    tc = operator.ChangeTextOperator()
    mutants = [mutant for mutant in tc.mutate(get_simple_dom())]
    assert 2 == len(mutants)
    assert "HelloMUTATED" == mutants[0].tree.find_by_tag(Tag.H1)[0].text
    assert "This is a DOM" == mutants[0].tree.find_by_tag(Tag.SPAN)[0].text
    assert "Hello" == mutants[1].tree.find_by_tag(Tag.H1)[0].text
    assert "This is a DOMMUTATED" == mutants[1].tree.find_by_tag(Tag.SPAN)[0].text


def get_simple_dom():
    return parse("""
    <html>
        <body>
            <h1>Hello</h1>
            <p><span>This is a DOM</span></p>
        </body>
    </html>""")
