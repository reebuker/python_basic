# 8
# Нужно, используя Counter и defaultdict, получить:
# ■ Количество каждого действия — сколько раз встречается view, click, message
# ■ Топ-2 популярных действий — самые частые действия с их количеством.
# ■ События, сгруппированные по пользователю— {user: [список действий/событий]} .
# ■ Доля message по каждой категории — для каждой категории считаем, какую долю от всех её событий составляют сообщения.
events = [
    {"user": "u1", "action": "view", "category": "electronics"},
    {"user": "u2", "action": "click", "category": "clothes"},
    {"user": "u1", "action": "click", "category": "electronics"},
    {"user": "u3", "action": "view", "category": "auto"},
    {"user": "u2", "action": "message", "category": "clothes"},
    {"user": "u1", "action": "message", "category": "electronics"},
]

from collections import Counter, defaultdict
from itertools import groupby

print(dict(Counter(x["action"] for x in events)))
print({sorted(Counter(x["action"] for x in events), key=lambda x: x[1])[:2]})
print({c: list(x["action"] for x in list(g)) for c,g in groupby(sorted(events, key=lambda x: x["user"]), key=lambda x: x["user"])})

