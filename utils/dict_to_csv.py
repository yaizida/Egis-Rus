import csv


def to_csv(data, path):
    # Сохранение словаря в CSV-файл
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Запись заголовка
        writer.writerow(data.keys())

        # Находим максимальную длину списка значений
        max_length = max(len(values) for values in data.values())

        # Запись значений для каждой строки
        for i in range(max_length):
            row = []
            for key in data:
                # Если индекс меньше длины списка, то записываем значение
                if i < len(data[key]):
                    row.append(data[key][i])
                # Иначе записываем пустое значение (например, '')
                else:
                    row.append('')
            writer.writerow(row)

    # Вывод сообщения о сохранении
    print("FCC сохранены в файл fcc_markets.csv")
