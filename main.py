import operator
import numpy as np
from enum import Enum

""" Общая структура и функции """
accurateness: str = '.6g'  # Точность до знака


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
    result = dict(sorted(dic.items(), key=operator.itemgetter(1), reverse=reverse))
    return result


def average_length(l_length: list, l_p: list) -> float:
    """ Средняя длина """
    L: float = 0.0

    s1: str = ''
    s2: str = ''
    for i in range(len(l_p)):
        L += len(l_length[i]) * l_p[i]

        s1 += f'{len(l_length[i])} * {l_p[i]} + '
        s2 += format(len(l_length[i]) * l_p[i], accurateness) + ' + '

    L = float(format(L, accurateness))

    print('L = ')
    print(s1, ' =\n', s2, ' = ', L, ' (бит)')
    print()

    return L


def entropy(l_p: list) -> float:
    """ Энтропия """
    H: float = 0.0

    s1: str = ''
    s2: str = ''
    for value in l_p:
        value = float(value)

        H += value * np.log2(value)

        s1 += f' - {value} * log2({value})'
        s2 += format(-value * np.log2(value), accurateness) + ' + '

    H = float(format(-H, accurateness))

    print('H = ')
    print(s1, ' =\n', s2, ' = ', H, ' (бит)')
    print()

    return H


def redundancy(L: float, H: float) -> float:
    """ Избыточность """
    K: float = float(format(L - H, accurateness))

    print('K =')
    print(f'{L} - {H} = ', K, ' (бит/символ)')
    print()

    return float(format(K, accurateness))


""" Код Шеннона-Фано """


def note_code(node: BinaryTreeNode, code: dict):
    """ Запись сверху-вниз """
    bi: SIDE = node.get_side()  # LEFT|RIGHT
    if bi is not None:
        for key in node.key.split():
            code[key] = code.get(key, '') + str(bi.value)


def shannon_fano_algorithm(sorted_ensemble: dict) -> dict:
    """ Для построения префиксного кода был использован обход дерева в глубину.
     Просто находим потомков узла и у его потомков ищем ещё потомков. """
    code: dict = dict()
    root = BinaryTreeNode(key=' '.join(sorted_ensemble.keys()), value=1.0)

    def recursion(node: BinaryTreeNode, level=0) -> None:
        full_p = node.value
        keys = node.key.split()

        if not node.visited and len(keys) != 1:
            summary: float = 0.0
            for n, key in enumerate(keys):
                p = sorted_ensemble[key]

                if abs(full_p / 2 - summary) - abs(full_p / 2 - (summary + p)) > 0:
                    summary += p
                else:
                    left_node = BinaryTreeNode(key=(' '.join(keys[0:n])),
                                               value=float(format(summary, accurateness)))
                    left_node.side = SIDE.LEFT

                    right_node = BinaryTreeNode(key=(' '.join(keys[n:len(keys)])),
                                                value=float(format(full_p - summary, accurateness)))
                    right_node.side = SIDE.RIGHT

                    node.children.append(left_node)
                    node.children.append(right_node)

                    break
        node.visited = True

        def enter_node(node: BinaryTreeNode, level: int):
            print(f'{str(node)}, Глубина: {level}, Сторона: {str(node.get_side())}')

        enter_node(node, level)
        # Запись кода идёт здесь
        note_code(node, code)

        for child in node.children:
            if child.visited:
                continue
            recursion(child, level + 1)

    recursion(root)

    return code


def shannon_fano_coding(*, input_ensemble: dict) -> dict:
    print('Неотсортированный: \n', input_ensemble)
    sorted_ensemble: dict = sort_dict_by_value(dic=input_ensemble, reverse=True)
    print('Отсортированный: \n', sorted_ensemble)
    print()
    result: dict = shannon_fano_algorithm(sorted_ensemble)
    print(result)

    l_prefix: list = [value for value in result.values()]
    p_l: list = [p for p in sorted_ensemble.values()]

    L: float = average_length(l_prefix, p_l)
    H: float = entropy(p_l)
    K: float = redundancy(L, H)

    return result


""" Код Хаффмена """


def bfs(root: BinaryTreeNode, enter_node=None) -> None:
    """ Обход в глубину в графе и запись кода """
    root.visited = True
    queue = [(root, 0)]
    while len(queue) != 0:
        target, level = queue.pop(0)

        if enter_node is not None:
            node, level = enter_node(target, level)

        for child in target.children:
            if child.visited:
                continue
            child.visited = True
            queue.append((child, level + 1))


def huffman_algorythm(sorted_ensemble: dict) -> dict:
    code: dict = dict()
    for key in sorted_ensemble.keys():
        code[key] = ''

    node_list: list = [BinaryTreeNode(key=ch, value=freq) for (ch, freq) in sorted_ensemble.items()]

    while len(node_list) > 1:
        node_list = sorted(node_list, key=lambda x: x.value, reverse=True)

        for node in node_list:
            print(str(node))

        count = 0
        for reversed_i in range(len(node_list) - 2, -1, -1):
            node_less = node_list[len(node_list) - 1 - count]
            node_bigger = node_list[reversed_i]

            new_node = BinaryTreeNode(key=(node_bigger.key + ' ' + node_less.key),
                                      value=float(format(node_bigger.value + node_less.value, accurateness)))

            keys1 = node_bigger.key.split()
            keys2 = node_less.key.split()

            if sorted_ensemble[keys1[0]] - sorted_ensemble[keys2[0]] > 0:
                print('Соединяемые элементы: \n', keys1, ' Левая часть: 0\n', keys2, ' Правая часть: 1')
                node_bigger.set_side(SIDE.LEFT)
                node_less.set_side(SIDE.RIGHT)
                for key in keys1:
                    code[key] = code.get(key, '') + '0'
                for key in keys2:
                    code[key] = code.get(key, '') + '1'
            else:
                print('Соединяемые элементы: \n', keys2, ' Левая часть: 0\n', keys1, ' Правая часть: 1')
                node_bigger.set_side(SIDE.RIGHT)
                node_less.set_side(SIDE.LEFT)
                for key in keys1:
                    code[key] = code.get(key, '') + '1'
                    print(code[key])
                for key in keys2:
                    code[key] = code.get(key, '') + '0'
                    print(code[key])
            print()

            new_node.children.append(node_bigger)
            new_node.children.append(node_less)

            node_list.pop(len(node_list) - 1 - count)
            node_list.pop(reversed_i)
            node_list.insert(reversed_i, new_node)

            break
        else:
            count += 1

    # bfs(node_list[0], enter_node=enter_node)

    for key, value in code.items():
        code[key] = value[::-1]
    return code


def huffman_coding(*, input_ensemble: dict) -> dict:
    print('Неотсортированный: \n', input_ensemble)
    sorted_ensemble: dict = sort_dict_by_value(dic=input_ensemble, reverse=True)
    print('Отсортированный: \n', sorted_ensemble)
    print()
    result: dict = huffman_algorythm(sorted_ensemble)
    print(result)

    l_prefix: list = [value for value in result.values()]
    p_l: list = [p for p in sorted_ensemble.values()]

    L: float = average_length(l_prefix, p_l)
    H: float = entropy(p_l)
    K: float = redundancy(L, H)

    return result


""" Вход-выход """


def test_valid(*, input_ensemble: dict) -> bool:
    summary: float = 0.0
    for value in input_ensemble.values():
        summary += float(value)
    summary = float(format(summary, accurateness))    
    return abs(1.0 - summary) < 1e-10


def main():
    suffix: int = 1
    # Читаем файл
    file_input = open(f'./input/input_{suffix}.txt', 'r')
    # Создаём массив непустных строк из файла
    lines = file_input.read().splitlines()
    # Закрываем файл
    file_input.close()

    # Создаём пустой словарь
    ensemble: dict = dict()

    # Добавляем ключ, значение в словарь
    for line in lines:
        line = line.split(':')
        for word in line:
            word.replace(' ', '')
        key, value = line
        ensemble[key] = float(value)

    # Сумма вероятностей должна быть равна 1.0
    if test_valid(input_ensemble=ensemble):
        num = int(input('>> Шеннон-Фано: 0; Хаффмен: 1 - '))
        prefix_dict: dict = dict()
        if num == 0:
            prefix_dict = shannon_fano_coding(input_ensemble=ensemble)
        elif num == 1:
            prefix_dict = huffman_coding(input_ensemble=ensemble)

        # Записываем результат (например,
        # z1: 001
        # z2: 010
        # ... )
        file_output = open(f'./output/output_{suffix}.txt', 'w')
        for key, value in prefix_dict.items():
            file_output.write(f'{key}: {value}\n')
        file_output.close()
    else:
        raise ValueError('Неверный вход!')


if __name__ == '__main__':
    main()
