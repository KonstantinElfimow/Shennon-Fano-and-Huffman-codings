""" Код Шеннона-Фано """
from tree_node import *
from useful_utils import *


accurateness: int = 6  # Округдение до знака


def _note_code(node: BinaryTreeNode, code: dict):
    """ Запись сверху-вниз """
    bi: SIDE = node.get_side()  # LEFT|RIGHT
    if bi is not None:
        for key in node.key.split():
            code[key] = code.get(key, '') + str(bi.value)


def _shannon_fano_algorithm(sorted_ensemble: dict) -> dict:
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
                                               value=round(summary, accurateness))
                    left_node.side = SIDE.LEFT

                    right_node = BinaryTreeNode(key=(' '.join(keys[n:len(keys)])),
                                                value=round(full_p - summary, accurateness))
                    right_node.side = SIDE.RIGHT

                    node.children.append(left_node)
                    node.children.append(right_node)

                    break
        node.visited = True

        def enter_node(node: BinaryTreeNode, level: int):
            print(f'{str(node)}, Глубина: {level}, Сторона: {str(node.get_side())}')

        enter_node(node, level)
        # Запись кода идёт здесь
        _note_code(node, code)

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
    result: dict = _shannon_fano_algorithm(sorted_ensemble)
    print(result)
    print()

    prefix_length: list = [len(value) for value in result.values()]
    if not kraft_inequality(prefix_length):
        raise ValueError('Кодовую информацию нельзя однозначно декодировать')
    p: list = [p for p in sorted_ensemble.values()]
    prefix_length_and_p = [tuple(x) for x in zip(prefix_length, p)]

    L: float = average_length(prefix_length_and_p)
    H: float = entropy(p)
    K: float = redundancy(L, H)

    return result
