from html_mutation.html.tags import Tag
from html_mutation.mutation import operator


def test_constructor_none():
    op = operator.ChangeTextOperator()
    assert len(op.tags) == 10


def test_contructor_ignore():
    op = operator.ChangeTextOperator(set([Tag.A, Tag.H6]))
    assert len(op.tags) == 8
