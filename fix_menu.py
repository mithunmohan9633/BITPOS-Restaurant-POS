path = 'core/templates/core/manage_menu.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("?{{", "\u20B9{{")
c = c.replace("Price (?)", "Price (\u20B9)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Fixed manage_menu.html")
