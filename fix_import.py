path = 'core/views.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the import line
if 'from django.shortcuts import render' in c:
    c = c.replace('from django.shortcuts import render', 'from django.shortcuts import render, redirect')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Fixed missing redirect import")
