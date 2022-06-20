import os
import tempfile

from html_mutation.html.dom import DomInfo, parse
from html_mutation.mutation.generator import MutantGenerator
from html_mutation.mutation.operator import (
    ChangeTextOperator,
    Mutant,
    Validity,
)
from html_mutation.mutation.validator import BaseValidator
from html_mutation.persistence.persistence import CsvPersistence


def test_generator():
    filename = os.path.join(tempfile.gettempdir(), "mutants.csv")
    if os.path.exists(filename):
        os.remove(filename)

    generator = MutantGenerator(
        get_simple_dom(),
        TrueValidator,
        CsvPersistence,
        {"filename": filename},
        {ChangeTextOperator()},
    )
    generator.execute()

    # TODO: read the content of the generated file
    # to make sure it contains what it should


def get_simple_dom():
    dom = parse(
        """
    <html>
        <body>
            <h1>Hello</h2>
            <p><span>This is a DOM</span></p>
        </body>
    </html>"""
    )

    return DomInfo("", dom, None)


class TrueValidator(BaseValidator):
    def __init__(self, dom_info: DomInfo) -> None:
        super().__init__(dom_info)

    def validate(dom_info: DomInfo, mutant: Mutant) -> Validity:
        return Validity.VALID


class FalseValidator(BaseValidator):
    def __init__(self, dom_info: DomInfo) -> None:
        super().__init__(dom_info)

    def validate(dom_info: DomInfo, mutant: Mutant) -> Validity:
        return Validity.INVALID
