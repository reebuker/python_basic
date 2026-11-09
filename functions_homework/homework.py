"""
ДЗ Функии
В `Corp_Summary.csv` лежит выгрузка по сотрудникам:
ФИО, департамент, команда, должность, оценка, оклад. Колонки разделены `;`.

Напишите программу, которая читает файл и по выбранному в аргументах варианту
готовит отчёт. На экран выводите так, как вам удобно читать.

Варианты отчётов такие. Основная функция должна принимать на вход
int - номер варианта. остальные параметры - по желанию:

1. Иерархия: для каждого департамента показать, какие команды в него входят.
2. Сводка по департаментам: название, сколько человек, минимальная
и максимальная зарплата, средняя по каждому департаменту.
3. То же самое, что в '2', но записанное в csv-файл.
Имя выходного файла можно захардкодить(например, константой в начале файла)
или передавать опциональным параметром в эту же функцию.

Чтение файла и каждый отчёт вынесите в отдельные функции.

в этой домашке главное - работа с функциями. про работу с файлами подробнее
поговорим в следующую среду на лекции
"""

import csv
import sys
from collections.abc import Iterator
from itertools import groupby


def read_file(filename: str) -> list[dict]:
    data = []
    try:
        with open(filename, newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            for row in reader:
                data.append(
                    {
                        "name": row[0],
                        "department": row[1],
                        "team": row[2],
                        "position": row[3],
                        "grade": float(row[4]),
                        "salary": int(row[5]),
                    }
                )

    except FileNotFoundError:
        print(f'Файла с названием: "{filename}" нет в рабочей директории')

    return data


def group_by(data: list[dict], key: str) -> indexerator:
    data = sorted(data, key=lambda x: x[key])
    return groupby(data, key=lambda x: x[key])


def hierarchy(data: list[dict]) -> None:
    grouped = group_by(data, "department")
    index = 1
    for dep, g in grouped:
        print(index, "Команды департамента", dep, ":")
        index += 1

        teams = set()
        for person in g:
            team = person["team"]
            if team not in teams:
                teams.add(team)
                print(team)
        print()


def report(data: list[dict]) -> None:
    grouped = group_by(data, "department")
    index = 1
    for dep, g in grouped:
        print(index, "Сводка по департаменту", dep)
        index += 1

        group = list(g)
        salaries = [person["salary"] for person in group]
        avg_salary = sum(salaries) / len(group)
        print(f"Численность: {len(group)} человек")
        print(f"Минимальная з/п: {min(salaries)} рублей")
        print(f"Максимальная з/п: {max(salaries)} рублей")
        print(f"Средняя з/п: {avg_salary:.2f} рублей")
        print()


def report_csv(data: list[dict], filename: str = "report.csv") -> None:
    grouped = group_by(data, key="department")
    header = [
        "Департамент",
        "Численность",
        "Минимальная з/п",
        "Максимальная з/п",
        "Средняя з/п",
    ]
    body = []
    for dep, g in grouped:
        group = list(g)
        salaries = [person["salary"] for person in group]
        row = []
        row.append(dep)
        row.append(len(group))
        row.append(min(salaries))
        row.append(max(salaries))
        row.append(sum(salaries) / len(group))
        body.append(row)

    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(header)
        writer.writerows(body)

    print("Written to file", filename)


def main(variant: int, data: list[dict]) -> None:
    match variant:
        case 1:
            hierarchy(data)
        case 2:
            report(data)
        case 3:
            report_csv(data)
        case _:
            print("Invalid argument. Use arguments 1/2/3")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid argument. Use arguments [1/2/3]")
        sys.exit()
    arg = int(sys.argv[1])
    data = read_file("Corp_Summary.csv")
    main(arg, data)
