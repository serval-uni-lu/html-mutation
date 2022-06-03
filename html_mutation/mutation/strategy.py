

from abc import abstractmethod


class BaseStrategy:
    def __init__(self, name: str, short_name: str, targets: set[str]) -> None:
        self.name = name
        self.short_name = short_name
        self.targets = {}

    @abstractmethod
    def mutate(dom: str):
        pass


class TextualContentStrategy(BaseStrategy):
    def __init__(self) -> None:
        name = 'Textual Content'
        short_name = 'TC'
        targets = set('a', 'h1', 'h2', 'h3', 'h4', 'th', 'p', 'span')
        super().__init__(name, short_name, targets)