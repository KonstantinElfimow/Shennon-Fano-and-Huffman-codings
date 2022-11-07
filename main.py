import numpy as np
from enum import Enum

accurateness: str = '.6g'


def sort_dict_by_value(ensemble: dict, reverse: bool) -> dict:
    """ Сортировка ансамбля по убыванию """
    result: dict = dict()

    sorted_keys = sorted(ensemble, key=ensemble.get, reverse=reverse)
    for w in sorted_keys:
        result[w] = ensemble[w]
    return result


def average_length(l_length: list, l_p: list) -> np.float64:
    """ Средняя длина """
    L: np.float64 = np.float64(0.0)

    s1: str = ''
    s2: str = ''
    for i in range(len(l_p)):
        L += len(l_length[i]) * l_p[i]

        s1 += f'{len(l_length[i])} * {l_p[i]} + '
        s2 += format(len(l_length[i]) * l_p[i], accurateness) + ' + '

    L = np.float64(format(L, accurateness))
    print(s1, ' =\n', s2, ' = ', L, ' (бит)')
    print()
    return L


def entropy(l_p: list) -> np.float64:
    """ Энтропия """
    H: np.float64 = np.float64(0.0)

    s1: str = ''
    s2: str = ''
    for value in l_p:
        value = np.float64(value)

        H += value * np.log2(value)

        s1 += f' - {value} * log2({value})'
        s2 += format(-value * np.log2(value), accurateness) + ' + '

    H = np.float64(format(-H, accurateness))

    print(s1, ' =\n', s2, ' = ', H, ' (бит)')
    print()

    return H


def redundancy(L: np.float64, H: np.float64) -> np.float64:
    """ Избыточность """
    K: np.float64 = np.float64(format(L - H, accurateness))
    print(f'{L} - {H} = ', K, ' (бит/символ)')
    print()
    return np.float64(format(K, accurateness))


""" Код Шеннона-Фано"""


_prefix_ensemble_shannon_fano: dict = dict()


def _shannon_fano_algorithm(sorted_ensemble: dict, start: int, stop: int, p: np.float64 = 1.0, level: int = 0,
                            bi: str = '') -> None:
    global _prefix_ensemble_shannon_fano
    print('Левая(0)/правая(1) ветка: ', bi, ' Глубина: ', level)

    keys: list = [key for key in sorted_ensemble.keys()]
    print(keys[start:stop], 'Вероятность: ', format(p, accurateness))

    for i in range(start, stop):
        _prefix_ensemble_shannon_fano[keys[i]] = _prefix_ensemble_shannon_fano.get(keys[i], '') + bi

    if stop - start <= 1:
        print(_prefix_ensemble_shannon_fano[keys[start]], '\n')
        return

    print()

    summary: np.float64 = np.float64(0.0)
    for i in range(start, stop, 1):
        value = sorted_ensemble.get(keys[i])

        if abs(p / 2 - summary) - abs(p / 2 - (summary + value)) > 0:
            summary += value
        else:
            _shannon_fano_algorithm(sorted_ensemble, start, i, summary, level + 1, '0')
            _shannon_fano_algorithm(sorted_ensemble, i, stop, np.float64(p - summary), level + 1, '1')
            break


def shannon_fano_algorithm(sorted_ensemble: dict) -> dict:
    _shannon_fano_algorithm(sorted_ensemble, 0, len(sorted_ensemble))
    return _prefix_ensemble_shannon_fano


def shannon_fano_coding(ensemble: dict) -> dict:
    print('Неотсортированный: \n', ensemble)

    sorted_ensemble: dict = sort_dict_by_value(ensemble, True)
    print('Отсортированный: \n', sorted_ensemble)
    print()

    result: dict = shannon_fano_algorithm(sorted_ensemble)
    print(result)

    l_prefix: list = [value for value in result.values()]
    p_l: list = [p for p in sorted_ensemble.values()]
    print('L = ')
    L: np.float64 = average_length(l_prefix, p_l)
    print('H = ')
    H: np.float64 = entropy(p_l)
    print('K =')
    K: np.float64 = redundancy(L, H)

    return result


""" Код Хаффмена """


class SIDE(Enum):
    def __str__(self):
        return str(self.value)

    LEFT = 'Левая часть'
    RIGHT = 'Правая часть'


class Node:
    def __init__(self, data):
        self.__visited = None
        self.__side = None
        self.key, self.value = data
        self.neighbours = []

    def set_side(self, side):
        self.__side = side

    def get_side(self):
        return self.__side

    side = property(fget=get_side, fset=set_side)

    # def set_visited(self, value):
    #     self.__visited = value
    #
    # def get_visited(self):
    #     return self.__visited
    #
    # visited = property(fget=get_visited, fset=set_visited)

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


class ListenableGraphNode(Node):
    def __init__(self, data=None):
        super().__init__(data)

    def set_side(self, value):
        super().set_side(value)

    def get_side(self):
        return super().get_side()

    side = property(fget=get_side, fset=set_side)

    # def set_visited(self, value):
    #     super().set_visited(value)
    #
    # def get_visited(self):
    #     return super().get_visited()
    #
    # visited = property(fget=get_visited, fset=set_visited)

    def __str__(self):
        return super().__str__()


def bfs(root: Node, enter_node=None):
    root.visited = True
    queue = [(root, 0)]
    while len(queue) != 0:
        target, level = queue.pop(0)
        safe_call(enter_node)(target, level)
        for neighbour in target.neighbours:
            if neighbour.visited:
                continue
            neighbour.visited = True
            queue.append((neighbour, level + 1))


def safe_call(function):
    def wrapper(*args):
        if function is not None:
            function(*args)
    return wrapper


def huffman_algorythm(sorted_ensemble: dict):
    code: dict = dict()
    for key in sorted_ensemble.keys():
        code[key] = ''

    node_list: list = [ListenableGraphNode([ch, freq]) for (ch, freq) in sorted_ensemble.items()]

    while len(node_list) > 1:
        node_list = sorted(node_list, key=lambda x: x.value, reverse=True)

        for node in node_list:
            print(str(node))

        count = 0
        for reversed_i in range(len(node_list) - 2, -1, -1):
            node_less = node_list[len(node_list) - 1 - count]
            node_bigger = node_list[reversed_i]

            new_node = ListenableGraphNode([(node_bigger.key + ' ' + node_less.key),
                                            float(format(node_bigger.value + node_less.value, accurateness))])

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

            new_node.neighbours.append(node_bigger)
            new_node.neighbours.append(node_less)

            node_list.pop(len(node_list) - 1 - count)
            node_list.pop(reversed_i)
            node_list.insert(reversed_i, new_node)

            break
        else:
            count += 1

    # def enter_node(node, level):
    #     print(f'{str(node)}, Высота: {level}, {str(node.get_side())}')

    # bfs(node_list[0], enter_node=enter_node)

    for key, value in code.items():
        code[key] = value[::-1]
    return code


def huffman_coding(ensemble: dict) -> dict:
    print('Неотсортированный: \n', ensemble)
    sorted_ensemble: dict = sort_dict_by_value(ensemble, True)
    print('Отсортированный: \n', sorted_ensemble)
    print()
    result: dict = huffman_algorythm(sorted_ensemble)
    print(result)

    l_prefix: list = [value for value in result.values()]
    p_l: list = [p for p in sorted_ensemble.values()]
    L: np.float64 = average_length(l_prefix, p_l)
    print('L = ', L, ' (бит)')
    H: np.float64 = entropy(p_l)
    print('H = ', H, ' (бит)')
    K: np.float64 = redundancy(L, H)
    print('K = L - H = ', K, ' (бит/символ)')

    return result


""" Вход-выход """


def test_valid(ensemble: dict) -> bool:
    summary: np.float64 = np.float64(0.0)
    for value in ensemble.values():
        summary += np.float64(value)
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
        ensemble[key] = np.float64(value)

    # Сумма вероятностей должна быть равна 1.0
    if test_valid(ensemble):
        num = int(input('>> Шеннон-Фано: 0; Хаффмен: 1 - '))
        prefix_dict: dict = dict()
        if num == 0:
            prefix_dict = shannon_fano_coding(ensemble)
        elif num == 1:
            prefix_dict = huffman_coding(ensemble)

        # Записываем результат (например,
        # z1: 001
        # z2: 010
        # ... )
        file_output = open(f'./output/output_{suffix}.txt', 'w')
        for key, value in prefix_dict.items():
            file_output.write(f'{key}: {value}\n')
        file_output.close()
    else:
        print('Неверный вход!')


if __name__ == '__main__':
    main()
