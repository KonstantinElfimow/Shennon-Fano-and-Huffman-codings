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
    def __init__(self, data: list):
        self.__visited = None
        self.__side = None
        self.key, self.value = data
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


def bfs(root, enter_node=None) -> None:
    """ Обход в глубину в графе и запись кода """
    root.visited = True
    queue = [(root, 0)]
    while len(queue) != 0:
        target, level = queue.pop(0)

        if enter_node is not None:
            node, level = enter_node(target, level)  # Запись кода идёт здесь

        for neighbour in target.children:
            if neighbour.visited:
                continue
            neighbour.visited = True
            queue.append((neighbour, level + 1))


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


""" Код Шеннона-Фано """

code: dict = dict()


def note_code(node):
    """ Запись сверху-вниз """
    bi: SIDE = node.get_side()  # LEFT|RIGHT
    if bi is not None:
        for key in node.key.split():
            code[key] = code.get(key, '') + str(bi.value)


def shannon_fano_algorithm(sorted_ensemble: dict) -> dict:
    """ Для построения префиксного кода был использован обход дерева в глубину.
     Просто находим потомков узла и у его потомков ищем ещё потомков. """
    global code
    root = BinaryTreeNode([' '.join(sorted_ensemble.keys()), np.float64(1.0)])

    def recursion(node, level=0) -> None:
        full_p = node.value
        keys = node.key.split()

        if not node.visited and len(keys) != 1:
            summary: np.float64 = np.float64(0.0)
            for n, key in enumerate(keys):
                p = sorted_ensemble[key]

                if abs(full_p / 2 - summary) - abs(full_p / 2 - (summary + p)) > 0:
                    summary += p
                else:
                    left_node = BinaryTreeNode([(' '.join(keys[0:n])),
                                                np.float64(format(summary, accurateness))])
                    left_node.side = SIDE.LEFT

                    right_node = BinaryTreeNode([(' '.join(keys[n:len(keys)])),
                                                 np.float64(format(full_p - summary, accurateness))])
                    right_node.side = SIDE.RIGHT

                    node.children.append(left_node)
                    node.children.append(right_node)

                    break
        node.visited = True

        def enter_node(node, level: int):
            print(f'{str(node)}, Глубина: {level}, Сторона: {str(node.get_side())}')

        # Запись кода идёт здесь
        enter_node(node, level)
        note_code(node)

        for child in node.children:
            if child.visited:
                continue
            recursion(child, level + 1)

    recursion(root)

    return code


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


def huffman_algorythm(sorted_ensemble: dict) -> dict:
    code: dict = dict()
    for key in sorted_ensemble.keys():
        code[key] = ''

    node_list: list = [BinaryTreeNode([ch, freq]) for (ch, freq) in sorted_ensemble.items()]

    while len(node_list) > 1:
        node_list = sorted(node_list, key=lambda x: x.value, reverse=True)

        for node in node_list:
            print(str(node))

        count = 0
        for reversed_i in range(len(node_list) - 2, -1, -1):
            node_less = node_list[len(node_list) - 1 - count]
            node_bigger = node_list[reversed_i]

            new_node = BinaryTreeNode([(node_bigger.key + ' ' + node_less.key),
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
