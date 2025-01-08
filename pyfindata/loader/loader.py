from typing import Protocol


class Loader(Protocol):

    def load(self, *args, **kwargs):
        pass
