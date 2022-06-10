from abc import abstractmethod

from html_mutation.html.tags import Tag


class BaseOperator:
    def __init__(
        self, name: str, short_name: str, ignored_tags: set[Tag]
    ) -> None:
        self.name = name
        self.short_name = short_name
        self.tags = self.default_tags() - (
            set() if ignored_tags is None else ignored_tags
        )

    @abstractmethod
    def mutate(self, dom: str):
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
