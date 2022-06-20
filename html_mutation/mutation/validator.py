from abc import abstractmethod

from html_mutation.html.dom import DomInfo
from html_mutation.html.driver import chrome_driver
from html_mutation.mutation.operator import Mutant, Validity


class BaseValidator:
    def __init__(self, dom_info: DomInfo) -> None:
        self.dom_info = dom_info

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def validate(mutant: Mutant) -> Validity:
        pass


class IsoRenderValidator(BaseValidator):
    def __init__(self, dom_info: DomInfo) -> None:
        super().__init__(dom_info)

    def __enter__(self):
        self.driver = chrome_driver()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()

    def validate(mutant: Mutant) -> Validity:
        pass
