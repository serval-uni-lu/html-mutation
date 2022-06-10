from multiprocessing import JoinableQueue, Process, cpu_count

from html_mutation.html.dom import DomInfo
from html_mutation.mutation.operator import BaseOperator


class MutantGenerator:
    def __init__(
        self, dom_info: DomInfo, operators: set[BaseOperator]
    ) -> None:
        self.dom_info = dom_info
        self.operators = operators

    def execute(self, number_process: int = 0):
        mutants_queue = JoinableQueue()
        self._create_mutants(mutants_queue)

        number_process = number_process if number_process > 0 else cpu_count()

        consumers = [
            Process(
                target=_validate_mutants,
                args=(mutants_queue, self.dom_info),
                daemon=True,
            )
            for _ in range(number_process)
        ]

        for p in consumers:
            p.start()

        for p in consumers:
            p.join()

    def _create_mutants(self, mutants_queue: JoinableQueue) -> None:
        for operator in self.operators:
            operator.mutate(self.dom_info)


def _validate_mutants(queue: JoinableQueue, dom_info: DomInfo) -> None:
    while True:
        try:
            res = queue.get(block=False)
            if res is None:
                break
            print(f"Consume {res}")
        except queue.Empty:
            pass
