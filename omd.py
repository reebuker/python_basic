''' 1 Задача '''
moscow = {201, 202, 203, 204}
kazan = {203, 204, 205, 206}

# что можно забрать в любом из двух городов
print(moscow & kazan)

# что есть только в Москве
print(moscow - kazan)

# что есть только в Казани
print(kazan - moscow)

# сколько разных товаров на обоих складах вместе
print(len(moscow | kazan))


''' 2 Задача '''
queries = [
    "чехол",
    "iphone",
    "чехол",
    "наушники",
    "iphone",
    "iphone",
    "кабель",
    "чехол",
    "iphone",
]

# сколько всего поисковых запросов в ленте
print(len(queries))

# сколько раз ввели каждый запрос
from collections import Counter
print(Counter(queries))

# какой запрос вводили чаще всего
print(Counter(queries).most_common(1))

# какую долю всех поисков он занимает
print(Counter(queries).most_common(1)[0][1] / len(queries))

# какие запросы встретились один раз
print([k for k, v in Counter(queries).items() if v == 1])


''' 3 Задача '''
orders = [
    {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
    {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
    {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
    {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
    {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
    {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
]

# на какую сумму оформили возвраты
print(sum(x["amount"] for x in orders if x["status"] == "returned"))

# кто хотя бы раз вернул заказ
print({x["buyer"] for x in orders if x["status"] == "returned"})

# сколько заказов доставлено покупателю
cnt_delivered = len([x for x in orders if x["status"] == "delivered"])
print(cnt_delivered)

# средний чек доставленных заказов
print(sum(x["amount"] for x in orders if x["status"] == "delivered") / cnt_delivered)


''' 4 Задача '''
days = [
    {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
    {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
    {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
    {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
    {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
]

# выручку за всю неделю
revenues = [x["revenue"] for x in days]
print(sum(revenues))

# день с самой большой выручкой
print([x["day"] for x in days if x["revenue"] == max(revenues)])

# среднюю выручку на один заказ в каждый день
res = {}
for day in days:
    res[day["day"]] = day["revenue"] / day["orders"] if day["orders"] > 0 else 0
print(res)

# дни, где возвратов больше 20% заказов
res = []
for day in days:
    if day["orders"] > 0 and day["returns"] / day["orders"] > 0.2:
        res.append(day["day"])
print(res)


''' 5 Задача '''
reviews = [
    {"id": 1, "product": "Чехол", "stars": 5},
    {"id": 1, "product": "Чехол", "stars": 3},
    {"id": 1, "product": "Чехол", "stars": 4},
    {"id": 2, "product": "Наушники", "stars": 2},
    {"id": 2, "product": "наушники", "stars": 2},
    {"id": 2, "product": "НАУШНИКИ", "stars": 5},
    {"id": 3, "product": "Планшет", "stars": 5},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 5, "product": "Кабель", "stars": 1},
]

# среднюю оценку каждого товара
reviews.sort(key=lambda x: x["id"])

from itertools import groupby

res = {}
for k, g in groupby(reviews, key=lambda x: x["product"].lower()):
    group = list(g)
    res[k] = sum(x["stars"] for x in group) / len(group)
print(res)

# худший товар по средней оценке среди тех, у кого хотя бы два отзыва
res = {}
for k, g in groupby(reviews, key=lambda x: x["product"].lower()):
    group = list(g)
    if len(group) >= 2:
        res[k] = sum(x["stars"] for x in group) / len(group)

print(min(res.items(), key=lambda x: x[1])[0])

# сколько отзывов на 1 или 2 звезды
low_cnt = len([x for x in reviews if x["stars"] in [1, 2]])
print(low_cnt)

# какую долю всех отзывов они составляют
print(low_cnt / len(reviews) if len(reviews) > 0 else 0)
