listings = [
    {"id": 1, "title": "iPhone 14", "price": 55000,
    "status": "active", "category": "phone"},
    {"id": 2, "title": "MacBook Pro", "price": 120000,
    "status": "sold", "category": "laptop"},
    {"id": 3, "title": "AirPods Pro", "price": 18000,
    "status": "active", "category": "audio"},
    {"id": 4, "title": "iPad mini", "price": 42000,
    "status": "active", "category": "tablet"},
    {"id": 5, "title": "Samsung Galaxy", "price": 35000,
    "status": "sold", "category": "phone"},
]

print(*list(x["price"] for x in listings if x["status"] == "active"))
print({x["id"]: x["title"] for x in listings if x["status"] == "active"})
print(sum(x["price"] for x in listings if x["status"] == "active"))
print(set(x["category"] for x in listings if x["status"] == "active"))
