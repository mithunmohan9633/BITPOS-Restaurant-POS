import os, glob

templates = glob.glob('core/templates/core/*.html')
for path in templates:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('>?<', '>-<')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated: {path}")
