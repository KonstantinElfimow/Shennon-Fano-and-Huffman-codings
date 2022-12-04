""" Код Хаффмена """
from useful_utils import *


accurateness: int = 6  # Округдение до знака


def _bfs(root: BinaryTreeNode, enter_node=None) -> None:
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


def _huffman_algorythm(sorted_ensemble: dict) -> dict:
    code: dict = dict()
    for key in sorted_ensemble.keys():
        code[key] = ''

    node_list: list = [BinaryTreeNode(key=ch, value=freq) for (ch, freq) in sorted_ensemble.items()]

    while len(node_list) > 1:
        node_list = sorted(node_list, key=lambda x: x.value, reverse=True)

        # for node in node_list:
        #     print(str(node))

        count = 0
        for reversed_i in range(len(node_list) - 2, -1, -1):
            node_less = node_list[len(node_list) - 1 - count]
            node_bigger = node_list[reversed_i]

            new_node = BinaryTreeNode(key=(node_bigger.key + ' ' + node_less.key),
                                      value=round(node_bigger.value + node_less.value, accurateness))

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
                    # print(code[key])
                for key in keys2:
                    code[key] = code.get(key, '') + '0'
                    # print(code[key])
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
    result: dict = _huffman_algorythm(sorted_ensemble)
    print(result)
    print()

    prefix_length: list = [len(value) for value in result.values()]
    p: list = [p for p in sorted_ensemble.values()]
    prefix_length_and_p = [tuple(x) for x in zip(prefix_length, p)]

    L: float = average_length(prefix_length_and_p)
    H: float = entropy(p)
    K: float = redundancy(L, H)

    return result
