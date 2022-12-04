""" Код Гилберта-Мура """
import numpy as np
import math
from useful_utils import average_length, entropy, redundancy, kraft_inequality


accurateness: int = 6  # Округдение до знака


def _gilbert_mur_algorithm(ensemble: dict) -> (dict, list):
    q: list = [0.0]
    sigma: list = list()
    for i, p in enumerate(ensemble.values()):
        q.append(round(q[i] + p, accurateness))
        sigma.append(round(q[i] + p / 2, accurateness))
    q.pop(len(q) - 1)
    l: list = [math.ceil(- np.log2(p) + 1) for p in ensemble.values()]

    prefix: dict = dict()
    for i, (alpha, p) in enumerate(ensemble.items()):
        code_word: str = ''
        length: float = 0.5
        step: float = 0.5
        print('Рассмотрим {}: {}. sigma = {}'.format(alpha, p, sigma[i]))
        count: int = 0
        print('итерация = {}, начальная длина отрезка = {}'.format(count, length))
        while 2 * step > p / 2:
            step /= 2
            count += 1
            if sigma[i] < length:
                code_word += '0'
                length -= step
            elif sigma[i] > length:
                code_word += '1'
                length += step
            length = round(length, accurateness)
            print('итерация = {}, длина отрезка = {}, этот шаг = {}, кодовое слово = {}'.format(count, length,
                                                                                                     step, code_word))

        print()
        prefix[alpha] = code_word

    table: list = list()
    table.append(tuple(['Xm', 'pm', 'qm', 'sigma', 'l', 'code']))
    for i, (alpha, word) in enumerate(prefix.items()):
        table.append(tuple([alpha, ensemble[alpha], q[i], sigma[i], l[i], word]))
    return prefix, tuple(table)


def gilbert_mur_coding(*, input_ensemble: dict) -> (tuple, float, float, float):
    print(input_ensemble)
    print()
    prefix, result_table = _gilbert_mur_algorithm(input_ensemble)
    print(prefix)
    print()

    prefix_length: list = [len(value) for value in prefix.values()]
    if not kraft_inequality(prefix_length):
        raise ValueError('Кодовую информацию нельзя однозначно декодировать')
    p: list = [p for p in input_ensemble.values()]
    prefix_length_and_p = [tuple(x) for x in zip(prefix_length, p)]

    L: float = average_length(prefix_length_and_p)
    H: float = entropy(p)
    K: float = redundancy(L, H)

    return result_table, L, H, K
