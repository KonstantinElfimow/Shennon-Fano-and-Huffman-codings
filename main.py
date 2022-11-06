import numpy as np


def sort_dict(ensemble: dict, reverse: bool) -> dict:
    """ Сортировка ансамбля по убыванию """
    result: dict = dict()

    sorted_keys = sorted(ensemble, key=ensemble.get, reverse=reverse)
    for w in sorted_keys:
        result[w] = ensemble[w]
    return result


def average_length(l_length: list, l_p: list) -> np.float64:
    L: np.float64 = np.float64(0.0)
    for i in range(len(l_p)):
        L += len(l_length[i]) * l_p[i]
    return np.float64(format(L, '.8g'))


def entropy(l_p: list) -> np.float64:
    H: np.float64 = np.float64(0.0)
    for value in l_p:
        value = np.float64(value)
        H += value * np.log2(value)
    H = np.float64(-H)
    return np.float64(format(H, '.8g'))


def redundancy(L: np.float64, H: np.float64) -> np.float64:
    K: np.float64 = np.float64(L - H)
    return np.float64(format(K, '.8g'))


_prefix_ensemble_shannon_fano: dict = dict()


def _division(ensemble: dict, start: int, stop: int, p: np.float64 = 1.0, level: int = 0, bi: str = '') -> None:
    global _prefix_ensemble_shannon_fano
    print('От какого до какого элемента: ', start + 1, stop, ' Левая(0)/правая(1) ветка: ', bi, ' Глубина: ', level)

    keys: list = [key for key in ensemble.keys()]
    print(keys[start:stop], 'Вероятность: ', format(p, '.5g'))

    for i in range(start, stop):
        _prefix_ensemble_shannon_fano[keys[i]] = _prefix_ensemble_shannon_fano.get(keys[i], '') + bi

    if stop - start <= 1:
        print(_prefix_ensemble_shannon_fano[keys[start]], '\n')
        return

    print()

    summary: np.float64 = np.float64(0.0)
    for i in range(start, stop, 1):
        value = ensemble.get(keys[i])

        if abs(p / 2 - summary) - abs(p / 2 - (summary + value)) > 0:
            summary += value
        else:
            _division(ensemble, start, i, summary, level + 1, '0')
            _division(ensemble, i, stop, np.float64(p - summary), level + 1, '1')
            break


def _shannon_fano_algorithm(ensemble) -> dict:
    _division(ensemble, 0, len(ensemble))
    return _prefix_ensemble_shannon_fano


def shannon_fano_coding(ensemble: dict) -> dict:
    print('Неотсортированный: \n', ensemble)

    sorted_ensemble: dict = sort_dict(ensemble, True)
    print('Отсортированный: \n', sorted_ensemble)
    print()

    result: dict = _shannon_fano_algorithm(sorted_ensemble)
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


_prefix_ensemble_huffman: dict = dict()


def huffman_coding(ensemble: dict) -> dict:
    print('Неотсортированный: \n', ensemble)

    sorted_ensemble: dict = sort_dict(ensemble, False)
    print('Отсортированный: \n', sorted_ensemble)
    print()

    result: dict = _shannon_fano_algorithm(sorted_ensemble)
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
        prefix_dict: dict = shannon_fano_coding(ensemble)
        # prefix_dict: dict = huffman_coding(ensemble)

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
