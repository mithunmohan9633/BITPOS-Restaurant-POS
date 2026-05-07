html = r"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>BITPOS - Point of Sale</title>
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
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

        /* Payment Modal */
        .payment-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(74, 59, 50, 0.6); backdrop-filter: blur(6px); z-index: 100; align-items: center; justify-content: center; }
        .payment-overlay.active { display: flex; }
        .payment-modal { background: var(--card-bg); border-radius: 20px; padding: 40px; width: 100%; max-width: 450px; box-shadow: 0 20px 60px rgba(74, 59, 50, 0.3); animation: slideUp 0.3s ease; }
        @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .payment-modal h2 { margin: 0 0 10px; font-weight: 800; font-size: 1.5rem; color: #4A3B32; text-align: center; }
        .payment-amount { text-align: center; font-size: 3rem; font-weight: 800; color: var(--primary); margin: 20px 0 30px; }
        .payment-label { text-align: center; color: #8A7A6F; font-weight: 600; margin-bottom: 5px; }
        .payment-methods { display: flex; gap: 20px; margin-bottom: 30px; }
        .payment-method { flex: 1; padding: 25px 15px; border-radius: 16px; border: 3px solid var(--border); text-align: center; cursor: pointer; transition: all 0.2s; background: #FAFAFA; }
        .payment-method:hover { border-color: var(--primary); transform: translateY(-3px); box-shadow: 0 8px 20px rgba(211, 140, 68, 0.15); }
        .payment-method.selected { border-color: var(--primary); background: #FFF5EC; box-shadow: 0 8px 20px rgba(211, 140, 68, 0.2); }
        .payment-method .method-icon { font-size: 2.5rem; margin-bottom: 10px; }
        .payment-method .method-name { font-weight: 800; font-size: 1.1rem; color: #4A3B32; }
        .payment-method .method-desc { font-size: 0.8rem; color: #8A7A6F; margin-top: 5px; }
        .confirm-payment-btn { width: 100%; padding: 18px; background: #4ECB71; color: white; border: none; border-radius: 12px; font-weight: 800; font-size: 1.2rem; cursor: pointer; transition: 0.2s; }
        .confirm-payment-btn:hover { background: #3DB85E; transform: translateY(-2px); }
        .confirm-payment-btn:disabled { background: var(--border); color: #8A7A6F; cursor: not-allowed; }
        .cancel-payment { width: 100%; padding: 12px; background: transparent; color: #C96459; border: none; font-weight: 800; font-size: 1rem; cursor: pointer; margin-top: 10px; }
        .cancel-payment:hover { text-decoration: underline; }

        /* Success Animation */
        .success-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(78, 203, 113, 0.95); z-index: 200; align-items: center; justify-content: center; flex-direction: column; }
        .success-overlay.active { display: flex; }
        .success-icon { font-size: 5rem; animation: popIn 0.5s ease; }
        @keyframes popIn { 0% { transform: scale(0); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
        .success-text { color: white; font-size: 2rem; font-weight: 800; margin-top: 20px; }
        .success-amount { color: white; font-size: 1.3rem; font-weight: 600; margin-top: 10px; opacity: 0.9; }
    </style>
</head>
<body>
    <header>
        <h1>BITPOS</h1>
        <div style='font-weight: 600; color: #8A7A6F; display: flex; align-items: center;'>
            {% if request.user.profile.role == 'admin' %}
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Menu</a>
            {% endif %}
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
                    <div class='item-price'>&#8377;{{ item.price }}</div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        <div class='order-panel'>
            <h2>New Order</h2>
            <div class='cart-items' id='cart-items'>
                <div style="margin:auto; opacity:0.5; font-weight:500;">Tap items to add to order</div>
            </div>
            <div class='cart-footer'>
                <div class='cart-total'>
                    <span>Total</span>
                    <span style="color:var(--primary)" id="cart-total-price">&#8377;0.00</span>
                </div>
                <button class='checkout-btn' id="checkout-btn" disabled onclick="openPayment()">Charge &#8377;0.00</button>
            </div>
        </div>
    </div>

    <!-- Payment Modal -->
    <div class="payment-overlay" id="payment-overlay">
        <div class="payment-modal">
            <h2>Complete Payment</h2>
            <div class="payment-label">Amount to Collect</div>
            <div class="payment-amount" id="payment-amount">&#8377;0.00</div>
            <div class="payment-methods">
                <div class="payment-method" id="method-cash" onclick="selectMethod('cash')">
                    <div class="method-icon">&#128176;</div>
                    <div class="method-name">Cash</div>
                    <div class="method-desc">Pay with cash</div>
                </div>
                <div class="payment-method" id="method-upi" onclick="selectMethod('upi')">
                    <div class="method-icon">&#128241;</div>
                    <div class="method-name">UPI</div>
                    <div class="method-desc">GPay / PhonePe / Paytm</div>
                </div>
            </div>
            <button class="confirm-payment-btn" id="confirm-payment-btn" disabled onclick="confirmPayment()">Select a Payment Method</button>
            <button class="cancel-payment" onclick="closePayment()">Cancel</button>
        </div>
    </div>

    <!-- Success Screen -->
    <div class="success-overlay" id="success-overlay">
        <div class="success-icon">&#10004;</div>
        <div class="success-text">Payment Successful!</div>
        <div class="success-amount" id="success-amount"></div>
    </div>

    <script>
        let cart = {};
        let selectedMethod = '';
        const RUPEE = '\u20B9';

        function addToCart(id, name, price) {
            if (cart[id]) { cart[id].qty += 1; }
            else { cart[id] = { name: name, price: parseFloat(price), qty: 1 }; }
            updateCartUI();
            try {
                let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + 0.1);
            } catch(e) {}
        }

        function removeFromCart(id) {
            if (cart[id]) { cart[id].qty -= 1; if (cart[id].qty <= 0) delete cart[id]; }
            updateCartUI();
        }

        function getTotal() {
            let total = 0;
            for (let id in cart) { total += cart[id].price * cart[id].qty; }
            return total;
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
                div.innerHTML = '<div style="display:flex; align-items:center;">' +
                    '<span class="cart-item-qty">' + item.qty + '</span>' +
                    '<div class="cart-item-info">' +
                    '<span class="cart-item-name">' + item.name + '</span>' +
                    '<span class="cart-item-price">' + RUPEE + itemTotal.toFixed(2) + '</span>' +
                    '</div></div>' +
                    '<div class="cart-remove" onclick="removeFromCart(\'' + id + '\')">&#10005;</div>';
                cartContainer.appendChild(div);
            }

            if (!hasItems) {
                cartContainer.innerHTML = '<div style="margin:auto; opacity:0.5; font-weight:500;">Tap items to add to order</div>';
                checkoutBtn.disabled = true;
                checkoutBtn.innerHTML = 'Charge ' + RUPEE + '0.00';
            } else {
                checkoutBtn.disabled = false;
                checkoutBtn.innerHTML = 'Charge ' + RUPEE + total.toFixed(2);
            }
            totalEl.innerText = RUPEE + total.toFixed(2);
        }

        function openPayment() {
            let total = getTotal();
            document.getElementById('payment-amount').innerText = RUPEE + total.toFixed(2);
            document.getElementById('payment-overlay').classList.add('active');
            selectedMethod = '';
            document.getElementById('method-cash').classList.remove('selected');
            document.getElementById('method-upi').classList.remove('selected');
            document.getElementById('confirm-payment-btn').disabled = true;
            document.getElementById('confirm-payment-btn').innerText = 'Select a Payment Method';
        }

        function closePayment() {
            document.getElementById('payment-overlay').classList.remove('active');
        }

        function selectMethod(method) {
            selectedMethod = method;
            document.getElementById('method-cash').classList.remove('selected');
            document.getElementById('method-upi').classList.remove('selected');
            document.getElementById('method-' + method).classList.add('selected');
            let total = getTotal();
            document.getElementById('confirm-payment-btn').disabled = false;
            if (method === 'cash') {
                document.getElementById('confirm-payment-btn').innerText = 'Confirm Cash ' + RUPEE + total.toFixed(2);
            } else {
                document.getElementById('confirm-payment-btn').innerText = 'Confirm UPI ' + RUPEE + total.toFixed(2);
            }
        }

        function confirmPayment() {
            let total = getTotal();
            let methodLabel = selectedMethod === 'cash' ? 'Cash' : 'UPI';
            closePayment();

            document.getElementById('success-amount').innerText = RUPEE + total.toFixed(2) + ' via ' + methodLabel;
            document.getElementById('success-overlay').classList.add('active');

            try {
                let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(523, audioCtx.currentTime);
                osc.frequency.setValueAtTime(659, audioCtx.currentTime + 0.15);
                osc.frequency.setValueAtTime(784, audioCtx.currentTime + 0.3);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + 0.5);
            } catch(e) {}

            setTimeout(function() {
                document.getElementById('success-overlay').classList.remove('active');
                cart = {};
                updateCartUI();
            }, 2000);
        }
    </script>
</body>
</html>"""

with open('core/templates/core/pos_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
