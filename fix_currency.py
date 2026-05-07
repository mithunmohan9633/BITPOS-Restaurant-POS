import os, glob

templates = glob.glob('core/templates/core/*.html')
for path in templates:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('${', '?{')
    c = c.replace('$<', '?<')
    c = c.replace("'$'", "'?'")
    c = c.replace('"$"', '"?"')
    c = c.replace('$0.00', '?0.00')
    c = c.replace("Charge $", "Charge ?")
    c = c.replace("Price ($)", "Price (?)")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated: {path}")
