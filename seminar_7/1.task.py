shown = {101, 102, 103, 104, 105}
clicked = {103, 105, 107}
messaged = {105, 107}

def show_no_click(shown, clicked):
    res = []
    for item in shown:
        if item not in clicked:
            res.append(item)
    return res

def clicked_no_message(clicked, messaged):
    res = []
    for item in clicked:
        if item not in messaged:
            res.append(item)
    return res

def message_no_show(messaged, shown):
    res = []
    for item in messaged:
        if item not in shown:
            res.append(item)
    return res

def all(shown, clicked, messaged):
    res = set() 
    for item in shown:
        res.add(item)
    for item in messaged:
        res.add(item)
    for item in clicked:
        res.add(item)
    return res

print(show_no_click(shown, clicked))
clicked_no_message(clicked, messaged)
message_no_show(messaged, shown)
all(shown, clicked, messaged)
