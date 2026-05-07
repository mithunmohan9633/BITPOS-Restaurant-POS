path = 'core/templates/core/pos_dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix innerText to innerHTML for HTML entity rendering
c = c.replace("balanceValue.innerText = 'Balanced &#10003;';", "balanceValue.innerHTML = 'Balanced \u2713';")
c = c.replace("balanceValue.innerText = 'Over by '", "balanceValue.innerHTML = 'Over by '")
c = c.replace("balanceValue.innerText = RUPEE + remaining", "balanceValue.innerHTML = RUPEE + remaining")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Fixed balance display")
