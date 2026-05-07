import os

path = 'core/templates/core/pos_dashboard.html'
html_code = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Nexus Cafe POS</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        :root { --bg-color: #FDF8F5; --card-bg: #FFFFFF; --text-color: #4A3B32; --primary: #D38C44; --border: #E8DCCB; }
        body { margin: 0; font-family: 'Outfit', sans-serif; background: var(--bg-color); color: var(--text-color); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        header { padding: 15px 30px; background: var(--card-bg); border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; z-index: 10; }
        h1 { margin: 0; font-weight: 800; font-size: 1.5rem; color: #4A3B32; }
        .main-container { display: flex; flex: 1; padding: 20px; gap: 20px; overflow: hidden; }
        .menu-section { flex: 2; display: flex; flex-direction: column; overflow-y: auto; padding-right: 10px; }
        .category-header { font-size: 1.2rem; font-weight: 800; margin: 10px 0; color: var(--primary); }
        .menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .menu-card { background: var(--card-bg); border: 2px solid var(--border); border-radius: 12px; padding: 15px; text-align: center; cursor: pointer; transition: all 0.2s; user-select: none; }
        .menu-card:active { transform: scale(0.95); }
        .menu-card:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(74, 59, 50, 0.1); }
        .item-name { font-weight: 600; margin-bottom: 5px; }
        .item-price { color: var(--primary); font-weight: 800; }
        
        .order-panel { flex: 1; background: var(--card-bg); border-radius: 16px; border: 2px solid var(--border); padding: 20px; display: flex; flex-direction: column; }
        .order-panel h2 { margin-top: 0; color: #4A3B32; border-bottom: 2px dashed var(--border); padding-bottom: 15px; }
        .cart-items { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; margin-bottom: 15px; }
        .cart-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; background: #FFF9F8; border-radius: 8px; border: 1px solid var(--border); }
        .cart-item-info { display: flex; flex-direction: column; }
        .cart-item-name { font-weight: 800; }
        .cart-item-price { color: var(--primary); font-weight: 600; font-size: 0.9rem; }
        .cart-item-qty { font-weight: 800; background: var(--border); padding: 2px 8px; border-radius: 4px; margin-right: 10px; }
        .cart-remove { color: #C96459; cursor: pointer; font-weight: 800; font-size: 1.2rem; margin-left: 10px; }
        
        .cart-footer { border-top: 2px dashed var(--border); padding-top: 15px; }
        .cart-total { display: flex; justify-content: space-between; font-size: 1.5rem; font-weight: 800; margin-bottom: 15px; color: #4A3B32; }
        .checkout-btn { width: 100%; padding: 15px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: 800; font-size: 1.2rem; cursor: pointer; transition: 0.2s; }
        .checkout-btn:hover { opacity: 0.9; }
        .checkout-btn:disabled { background: var(--border); color: #8A7A6F; cursor: not-allowed; }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS <span style='color: var(--primary)'>?</span></h1>
        <div style='font-weight: 600; color: #8A7A6F; display: flex; align-items: center;'>
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Menu</a>
            <span style='margin-right:20px'>Direct Sale Mode</span>
            <a href='/logout/' style='color:#C96459;text-decoration:none;font-weight:800;padding:8px 12px;background:#FFF9F8;border-radius:8px'>Logout</a>
        </div>
    </header>
    <div class='main-container'>
        <div class='menu-section'>
            {% for category in categories %}
            <div class='category-header'>{{ category.name }}</div>
            <div class='menu-grid'>
                {% for item in category.items.all %}
                <div class='menu-card' onclick="addToCart('{{ item.id }}', '{{ item.name|escapejs }}', {{ item.price }})">
                    <div class='item-name'>{{ item.name }}</div>
                    <div class='item-price'>${{ item.price }}</div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        <div class='order-panel'>
            <h2>New Order</h2>
            <div class='cart-items' id='cart-items'>
                <div style="margin:auto; opacity:0.5; font-weight:500;" id="empty-cart-msg">Tap items to add to order</div>
            </div>
            <div class='cart-footer'>
                <div class='cart-total'>
                    <span>Total</span>
                    <span style="color:var(--primary)" id="cart-total-price">$0.00</span>
                </div>
                <button class='checkout-btn' id="checkout-btn" disabled onclick="processCheckout()">Charge $0.00</button>
            </div>
        </div>
    </div>

    <script>
        let cart = {};

        function addToCart(id, name, price) {
            if (cart[id]) {
                cart[id].qty += 1;
            } else {
                cart[id] = { name: name, price: parseFloat(price), qty: 1 };
            }
            updateCartUI();
            
            // Play a soft click sound for satisfying feedback
            try {
                let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                let oscillator = audioCtx.createOscillator();
                let gainNode = audioCtx.createGain();
                oscillator.type = 'sine';
                oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
                gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.start();
                oscillator.stop(audioCtx.currentTime + 0.1);
            } catch(e) {}
        }

        function removeFromCart(id) {
            if (cart[id]) {
                cart[id].qty -= 1;
                if (cart[id].qty <= 0) {
                    delete cart[id];
                }
            }
            updateCartUI();
        }

        function updateCartUI() {
            const cartContainer = document.getElementById('cart-items');
            const totalEl = document.getElementById('cart-total-price');
            const checkoutBtn = document.getElementById('checkout-btn');

            cartContainer.innerHTML = '';
            
            let total = 0;
            let hasItems = false;

            for (let id in cart) {
                hasItems = true;
                let item = cart[id];
                let itemTotal = item.price * item.qty;
                total += itemTotal;

                let div = document.createElement('div');
                div.className = 'cart-item';
                div.innerHTML = `
                    <div style="display:flex; align-items:center;">
                        <span class="cart-item-qty">${item.qty}</span>
                        <div class="cart-item-info">
                            <span class="cart-item-name">${item.name}</span>
                            <span class="cart-item-price">$${itemTotal.toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="cart-remove" onclick="removeFromCart('${id}')">?</div>
                `;
                cartContainer.appendChild(div);
            }

            if (!hasItems) {
                cartContainer.innerHTML = '<div style="margin:auto; opacity:0.5; font-weight:500;" id="empty-cart-msg">Tap items to add to order</div>';
                checkoutBtn.disabled = true;
                checkoutBtn.innerHTML = `Charge $0.00`;
            } else {
                checkoutBtn.disabled = false;
                checkoutBtn.innerHTML = `Charge $${total.toFixed(2)}`;
            }
            
            totalEl.innerText = `$${total.toFixed(2)}`;
        }

        function processCheckout() {
            alert("Payment processed successfully! Printing receipt...");
            cart = {};
            updateCartUI();
        }
    </script>
</body>
</html>"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(html_code)
