from html_mutation.html.dom import DomInfo
from html_mutation.mutation.operator import BaseStrategy


class MutantGenerator:
    def __init__(self, dom_info: DomInfo, strategies: set[BaseStrategy]) -> None:
        self.domInfo = dom_info
        self.strategies = strategies

    def execute():
        pass
