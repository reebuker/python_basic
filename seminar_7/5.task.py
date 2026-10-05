# 5
# Используя zip и comprehension'ы, получить:
# ■ Отчёт по каждому месяцу — выполнена ли цель, и с какой разницей:
# формат строки:
# "Mar: план выполнен (+40 000)"
# ■ Месяцы, где выручка выросла И план выполнен
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [1200000, 950000, 1340000, 1780000, 1560000, 2100000]
target = [1000000, 1000000, 1300000, 1600000, 1600000, 2000000]

n = len(months)

is_done = (True for i in range(n) if revenue[i] - target[i] > 0 else False)
diff = (revenue[i] - target[i] for i in range(n))
    
