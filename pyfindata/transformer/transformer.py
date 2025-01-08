from typing import Protocol


class Transformer(Protocol):

    def transform(self):
        pass
    