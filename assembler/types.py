from typing import Iterable


class FrozenDeque:
    """An immutable variant of deque with ability to save and restore state."""

    def __init__(self, iterable: Iterable):
        self._deque = tuple(iterable)
        self._head = 0
        self._tail = len(self._deque)

    def __len__(self):
        return self._tail - self._head

    def __repr__(self):
        visible_elements = self._deque[self._head:self._tail]
        body = ", ".join(map(str, visible_elements))
        return f"FrozenDeque[{body}]"

    @property
    def state(self):
        return self._head, self._tail

    def restore_state(self, state):
        self._head, self._tail = state

    def pop(self):
        if len(self) == 0:
            raise IndexError("pop from empty FrozenDeque")

        self._tail -= 1
        return self._deque[self._tail]

    def lpop(self):
        if len(self) == 0:
            raise IndexError("pop from empty FrozenDeque")

        popped = self._deque[self._head]
        self._head += 1
        return popped
