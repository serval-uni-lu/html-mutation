import enum

from abc import abstractmethod
from copy import deepcopy
from typing import Iterator, Union
from xml.etree.ElementTree import Element

from html_mutation.html.dom import DomTree
from html_mutation.html.tags import Tag

class Validity(enum.Enum):
    VALID = "valid"
    INVALID = "invalid"


class Mutant:
    def __init__(self, tree: DomTree, xpath: str, strategy: str) -> None:
        self.tree = tree
        self.xpath = xpath
        self.strategy = strategy


class MutantEntry:
    def __init__(self, mutant: Mutant, validity: Validity) -> None:
        self.xpath = mutant.xpath
        self.strategy = mutant.strategy
        self.validity = validity


class BaseOperator:
    def __init__(
        self, name: str, short_name: str, ignored_tags: set[Tag]
    ) -> None:
        self.name = name
        self.short_name = short_name
        self.tags = self.default_tags() - (
            set() if ignored_tags is None else ignored_tags
        )

    def mutate(self, dom: DomTree) -> Iterator[Mutant]:
        for node in dom.find_by_tag(self.tags):
            mutant = self._mutate_node(dom, node)
            if mutant:
                yield mutant

    @abstractmethod
    def _mutate_node(self, dom: DomTree) -> Union[None, Mutant]:
        pass

    @abstractmethod
    def default_tags(self) -> set[Tag]:
        pass


class ChangeTextOperator(BaseOperator):
    def __init__(self, ignored_tags: set[Tag] = None) -> None:
        super().__init__("Textual Content", "TC", ignored_tags)

    def default_tags(self):
        return set(
            [
                Tag.A,
                Tag.H1,
                Tag.H2,
                Tag.H3,
                Tag.H4,
                Tag.H5,
                Tag.H6,
                Tag.TH,
                Tag.P,
                Tag.SPAN,
            ]
        )

    def _mutate_node(
        self, tree: DomTree, node: Element
    ) -> Union[None, Mutant]:
        if not node.text:
            return None

        mutated = deepcopy(tree)
        xpath = tree.get_xpath(node)
        target = mutated.find_by_xpath(xpath)[0]
        target.text = target.text + "MUTATED"
        return Mutant(mutated, xpath, self.short_name)
