""" Общая структура и функции """
from enum import Enum
import numpy as np


accurateness: int = 6  # Округдение до знака


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
        self.children = []

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


def sort_dict_by_value(*, dic: dict, reverse: bool) -> dict:
    """ Сортировка ансамбля по ключу """
    result = dict(sorted(dic.items(), key=lambda key_value: key_value[1], reverse=reverse))
    return result


def average_length(length_and_p: list) -> float:
    """ Средняя длина """
    L: float = round(sum([round(x[0] * x[1], accurateness) for x in length_and_p]), accurateness)
    s1: str = ' + '.join([f'{x[0]} * {x[1]}' for x in length_and_p])
    s2: str = ' + '.join([f'{round(x[0] * x[1], accurateness)}' for x in length_and_p])

    print('L = {} = {} = {} (бит)'.format(s1, s2, L))
    print()

    return L


def entropy(p: list) -> float:
    """ Энтропия """
    H: float = round(sum([round(-x * np.log2(x), accurateness) for x in p]), accurateness)
    s1: str = '- (' + ' + '.join([f'{x} * log2({x})' for x in p]) + ')'
    s2: str = ' + '.join([f'{round(-x * np.log2(x), accurateness)}' for x in p])

    print('H = {} = {} = {} (бит)'.format(s1, s2, H))
    print()

    return H


def redundancy(L: float, H: float) -> float:
    """ Избыточность """
    K: float = round(L - H, accurateness)

    print('K = {} - {} = {} (бит/символ)'.format(L, H, K))
    print()

    return K
