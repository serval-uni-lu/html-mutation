from abc import abstractmethod

class BaseComparator:
    def __init__(self) -> None:
        self._memory = Memory()

    @abstractmethod
    def compare(self, path1: str, path2: str) -> bool:
        pass


class ImageComparator:
    def compare(self, path1: str, path2: str) -> bool:
        pass


class HtmlComparator:
    def compare(self, path1: str, path2: str) -> bool:
        pass

class Memory:
    def __init__(self) -> None:
        self._table = {}

    def save(self, path1: str, path2: str, is_same: bool) -> None:
        self._table[frozenset({path1, path2})] = is_same

    def get(self, path1: str, path2: str) -> bool:
        return self._table[frozenset({path1, path2})]

    def is_saved(self, path1: str, path2: str) -> bool:
        return frozenset({path1, path2}) in self._table
