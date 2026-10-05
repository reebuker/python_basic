visit_log = [
"user_42", "user_15", "user_42", "user_8",
"user_15", "user_33", "user_15", "user_8"
]
day1 = ["user_42", "user_15", "user_42", "user_8"]
day2 = ["user_15", "user_33", "user_15", "user_8"]

print(set(visit_log) | set(day1) | set(day2))
print(dict.fromkeys(visit_log).keys())
print(set(day1) & set(day2))
print(set(x for x in day1 if day1.count(x) > 1) | set(x for x in day2 if day2.count(x) > 1))
print(set(day1) - set(day2))
