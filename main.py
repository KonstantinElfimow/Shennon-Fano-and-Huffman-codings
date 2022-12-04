""" Вход-выход """
from functools import reduce

from shannon_fano_coding import shannon_fano_coding
from huffman_coding import huffman_coding
from gilbert_mur_coding import gilbert_mur_coding


accurateness: int = 6  # Округдение до знака


def test_valid(*, input_ensemble: dict) -> bool:
    summary: float = round(reduce(lambda x, y: x + y, input_ensemble.values()), accurateness)
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
        num = int(input('>> Шеннон-Фано: 0; Хаффмен: 1; Гилберт-Мур: 2 - '))
        if num == 0 or num == 1:
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
            file_output.write('\n'.join('{}: {}'.format(k, v) for k, v in prefix_dict.items()))
            file_output.close()
        elif num == 2:
            result_table: tuple = gilbert_mur_coding(input_ensemble=ensemble)
            # Записываем результат
            file_output = open(f'./output/output_{suffix}.txt', 'w')
            file_output.write('\n'.join(['    '.join([x for x in row]) for row in result_table]))
            file_output.close()
        else:
            raise ValueError
    else:
        raise ValueError('Неверный вход!')


if __name__ == '__main__':
    main()
