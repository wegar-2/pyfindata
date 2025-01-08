from typing import Protocol


class Pipeline(Protocol):

    def execute(self):
        pass
