from multiprocessing import Manager, Process, Queue, Value, cpu_count
from queue import Empty

from html_mutation.html.dom import DomInfo
from html_mutation.mutation.operator import BaseOperator


class MutantGenerator:
    def __init__(
        self, dom_info: DomInfo, operators: set[BaseOperator]
    ) -> None:
        self.dom_info = dom_info
        self.operators = operators

    def execute(self, number_process: int = 0):
        number_process = number_process if number_process > 0 else cpu_count()

        with Manager() as manager:
            mutant_queue = manager.Queue()
            is_running = manager.Value(bool, True, lock=False)

            consumers = [
                Process(
                    target=_validate_mutants,
                    args=(mutant_queue, self.dom_info, is_running),
                    daemon=True,
                )
                for _ in range(number_process)
            ]

            for p in consumers:
                p.start()

            self._create_mutants(mutant_queue, is_running)

            for p in consumers:
                p.join()

    def _create_mutants(self, mutant_queue: Queue, is_running: Value) -> None:
        try:
            for operator in self.operators:
                for mutant in operator.mutate(self.dom_info.dom):
                    mutant_queue.put(mutant)
        finally:
            is_running.value = False


def _validate_mutants(
    mutant_queue: Queue, dom_info: DomInfo, is_running: Value
) -> None:
    while is_running.value:
        try:
            res = mutant_queue.get(block=False)
            if res is None:
                break
            print(f"Consume {res}")
        except Empty:
            pass
