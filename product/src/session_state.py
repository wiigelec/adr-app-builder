from __future__ import annotations

import copy
from typing import Callable


class ApplicationSession:
    # Mechanical harness for active working state versus persisted Dataset state.
    def __init__(self, persisted_reader: Callable[[], object], persisted_writer: Callable[[object], None]):
        self._reader = persisted_reader
        self._writer = persisted_writer
        self._active = copy.deepcopy(self._reader())

    def read(self):
        return copy.deepcopy(self._active)

    def edit(self, editor: Callable[[object], None]):
        editor(self._active)
        return self.read()

    def save(self):
        self._writer(copy.deepcopy(self._active))

    def reopen(self):
        self._active = copy.deepcopy(self._reader())
        return self.read()
