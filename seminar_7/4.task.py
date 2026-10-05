# 4
# Используя enumerate, zip и comprehension'ы, получить:
# ■ {индекс: категория} — словарь, где ключ — позиция, значение — категория
# ■ {категория: индекс} — обратный словарь
# ■ {категория: бюджет} — сопоставление категории с её бюджетом
# ■ Только категории с бюджетом выше среднего
categories = ["electronics", "clothes", "furniture", "auto", "sport"]
budgets = [500000, 200000, 150000, 800000, 100000]

print({k: v for k,v in enumerate(categories)})
print({v: k for k,v in enumerate(categories)})
mapa = {k: v for k,v in zip(categories, budgets)} 
print(mapa)
print(list(k for k, v in mapa.items() if v > sum(mapa.values()) / len(mapa)))

