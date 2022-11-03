import numpy as np

# Коэф для более точного рассчёта float
k: int = 100000


def descending_sort(ensemble: dict) -> dict:
    """ Сортировка ансамбля по убыванию """
    result: dict = dict()

    sorted_keys = sorted(ensemble, key=ensemble.get, reverse=True)
    for w in sorted_keys:
        result[w] = ensemble[w]
    return result


def average_length(l_length: list, l_p: list) -> float:
    L: float = 0.0
    for i in range(len(l_p)):
        L += len(l_length[i]) * k * l_p[i]
    L /= k
    return float(format(L, '.8g'))


def entropy(l_p: list) -> float:
    H: float = 0.0
    for value in l_p:
        H += k * value * np.log2(value)
    H = -H / k
    return float(format(H, '.8g'))


def redundancy(L: float, H: float) -> float:
    K: float = L - H
    return float(format(K, '.8g'))


_prefix_ensemble: dict = dict()


def _division(ensemble: dict, start: int, stop: int, p: float = 1.0, level: int = 0, bi: str = "") -> None:
    global _prefix_ensemble
    print("От какого до какого элемента: ", start + 1, stop, " Левая(0)/правая(1) ветка: ", bi, " Глубина: ", level)

    keys: list = [key for key in ensemble.keys()]
    print(keys[start:stop], "Вероятность: ", format(p, '.5g'))

    for i in range(start, stop):
        _prefix_ensemble[keys[i]] = _prefix_ensemble.get(keys[i], "") + bi

    if stop - start <= 1:
        print(_prefix_ensemble[keys[start]], "\n")
        return

    print()

    summary: float = 0.0
    for i in range(start, stop, 1):
        value = ensemble.get(keys[i])

        if abs(p / 2 * k - summary * k) - abs(p / 2 * k - (summary * k + value * k)) > 0:
            summary += value
        else:
            _division(ensemble, start, i, summary, level + 1, "0")
            _division(ensemble, i, stop, (k * p - k * summary) / k, level + 1, "1")
            break


def _shannon_fano_algorithm(ensemble) -> dict:
    _division(ensemble, 0, len(ensemble))
    return _prefix_ensemble


def shannon_fano_coding(ensemble: dict) -> dict:
    print("Неотсортированный: \n", ensemble)

    sorted_ensemble: dict = descending_sort(ensemble)
    print("Отсортированный: \n", sorted_ensemble)
    print()

    result: dict = _shannon_fano_algorithm(sorted_ensemble)
    print(result)

    l_prefix: list = [value for value in result.values()]
    p_l: list = [p for p in sorted_ensemble.values()]
    L: float = average_length(l_prefix, p_l)
    print("L = ", L, " (бит)")
    H: float = entropy(p_l)
    print("H = ", H, " (бит)")
    K: float = redundancy(L, H)
    print("K = L - H = ", K, " (бит/символ)")

    return result


def huffman_coding(ensemble: dict) -> dict:
    pass


def test_valid(ensemble: dict) -> bool:
    summary: float = 0
    for value in ensemble.values():
        summary += value * k
    return k - summary < 1e-14


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
        print("Неверный вход!")


if __name__ == '__main__':
    main()
