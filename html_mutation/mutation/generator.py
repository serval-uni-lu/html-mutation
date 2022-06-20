from multiprocessing import Lock, Manager, Process, Queue, Value, cpu_count
from queue import Empty

from html_mutation.html.dom import DomInfo
from html_mutation.mutation.operator import BaseOperator, MutantEntry


class MutantGenerator:
    def __init__(
        self,
        dom_info: DomInfo,
        validator: type,
        persistor: type,
        persistor_args: dict,
        operators: set[BaseOperator],
    ) -> None:
        self.dom_info = dom_info
        self.operators = operators
        self.validator = validator
        self.persistor = persistor
        self.persistor_args = persistor_args

    def execute(self, number_process: int = 0):
        number_process = number_process if number_process > 0 else cpu_count()

        with Manager() as manager:
            mutant_queue = manager.Queue()
            validated_queue = manager.Queue()
            is_generating = manager.Value(bool, True, lock=False)
            validator_count = manager.Value(int, 0)
            lock = manager.Lock()

            validators = [
                Process(
                    target=_validate_mutants,
                    args=(
                        self.dom_info,
                        self.validator,
                        mutant_queue,
                        validated_queue,
                        is_generating,
                        validator_count,
                        lock,
                    ),
                )
                for _ in range(number_process)
            ]

            persitor = Process(
                target=_persist_mutants,
                args=(
                    self.dom_info,
                    self.persistor,
                    self.persistor_args,
                    validated_queue,
                    is_generating,
                    validator_count,
                ),
            )

            for v in validators:
                v.start()

            persitor.start()
            self._create_mutants(mutant_queue, is_generating)

            for v in validators:
                v.join()

            persitor.join()

    def _create_mutants(
        self, mutant_queue: Queue, is_generating: Value
    ) -> None:
        try:
            for operator in self.operators:
                for mutant in operator.mutate(self.dom_info.dom):
                    mutant_queue.put(mutant)
        finally:
            is_generating.value = False


def _validate_mutants(
    dom_info: DomInfo,
    validator: type,
    mutant_queue: Queue,
    validated_queue: Queue,
    is_generating: Value,
    validator_count: Value,
    lock: Lock,
) -> None:
    try:
        with lock:
            validator_count.value += 1
        with validator(dom_info) as v:
            while is_generating.value or not mutant_queue.empty():
                try:
                    mutant = mutant_queue.get(block=False)
                    if mutant is None:
                        continue
                    validity = v.validate(mutant)
                    validated_queue.put(MutantEntry(mutant, validity))
                except Empty:
                    pass
    finally:
        with lock:
            validator_count.value -= 1


def _persist_mutants(
    dom_info: DomInfo,
    persistor: type,
    persistor_args: dict,
    validated_queue: Queue,
    is_generating: Value,
    validator_count: Value,
) -> None:
    with persistor(dom_info, **persistor_args) as p:
        while (
            is_generating.value
            or validator_count.value > 0
            or not validated_queue.empty()
        ):
            try:
                mutant = validated_queue.get(block=False)
                if mutant is None:
                    continue
                p.persist(mutant)
            except Empty:
                pass
