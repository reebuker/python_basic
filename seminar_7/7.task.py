# 7
# Дан список продавцов с полями name, category, rating, sales:
# Используя sorted, key и itertools.groupby, получить:
# ■ Топ-3 продавца по продажам
# ■ Сортировка по категории, а внутри
# категории — по рейтингу (убывание)
# ■ Лучший продавец в каждой категории — для каждой категории найти продавца с
# максимальным рейтингом
sellers = [
    {"name": "TechShop", "category": "electronics", "rating": 4.8, "sales": 1240},
    {"name": "ModaStore", "category": "clothes", "rating": 4.5, "sales": 830},
    {"name": "AutoParts", "category": "auto", "rating": 4.2, "sales": 415},
    {"name": "GadgetZone", "category": "electronics", "rating": 4.6, "sales": 970},
    {"name": "SportLife", "category": "sport", "rating": 4.5, "sales": 610},
]

print(list(x["name"] for x in sorted(sellers, key=lambda x: x["sales"], reverse=True)[:3]))

from itertools import groupby
sellers = sorted(sellers, key=lambda x: x["category"])
sellers = sorted(sellers, key=lambda x: x["rating"], reverse=True)
print(sellers)

# Уже отсортированный после 2 задания
print({c: list(g)[0]["name"] for c, g in groupby(sellers, key=lambda x: x["category"])})


