from enum import Enum


class SIDE(Enum):
    LEFT = 0
    RIGHT = 1

    def __str__(self):
        if self.value == 0:
            return 'Лево'
        else:
            return 'Право'


class BinaryTreeNode:
    def __init__(self, *, key: int | str, value: int | float):
        self.__visited = None
        self.__side = None
        self.key, self.value = key, value
        self.children: list = []
        self.parents: list = []

    def set_side(self, side):
        self.__side = side

    def get_side(self):
        return self.__side

    side = property(fget=get_side, fset=set_side)

    def set_visited(self, value):
        self.__visited = value

    def get_visited(self):
        return self.__visited

    visited = property(fget=get_visited, fset=set_visited)

    def __str__(self) -> str:
        return '{}: {}'.format(self.key, self.value)