import csv

from abc import abstractmethod
from fileinput import filename
from html_mutation.html.dom import DomInfo

from html_mutation.mutation.operator import MutantEntry

class BasePersistence:
    def __init__(self, dom_info: DomInfo) -> None:
        self.dom_info = dom_info
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def persist(self, mutant: MutantEntry) -> None:
        pass

class CsvPersistence:
    def __init__(self, dom_info: DomInfo, filename: str) -> None:
        self.dom_info = dom_info
        self.filename = filename
    
    def __enter__(self):
        self.file = open(self.filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["dom_id", "mutant_operator", "mutant_location", "valid"])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    @abstractmethod
    def persist(self, mutant: MutantEntry):
        self.writer.writerow([self.dom_info.dom_id, mutant.strategy, mutant.xpath, mutant.validity.value])