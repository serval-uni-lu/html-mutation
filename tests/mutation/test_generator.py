
from html_mutation.mutation.generator import MutantGenerator
from html_mutation.mutation.operator import ChangeTextOperator
from html_mutation.html.dom import DomInfo, parse

def test_generator():
    generator = MutantGenerator(get_simple_dom(), {ChangeTextOperator()})
    generator.execute()


def get_simple_dom():
    dom = parse("""
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>""")

    return DomInfo("", dom, None)