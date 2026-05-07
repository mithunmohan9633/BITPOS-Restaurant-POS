path = 'core/templates/core/pos_dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_confirm = """        function confirmPayment() {
            let total = getTotal();
            let cashVal = parseFloat(document.getElementById('input-cash').value) || 0;
            let upiVal = parseFloat(document.getElementById('input-upi').value) || 0;

            closePayment();

            document.getElementById('success-amount').innerText = RUPEE + total.toFixed(2);
            let detail = '';
            if (methods.cash && methods.upi) {
                detail = 'Cash: ' + RUPEE + cashVal.toFixed(2) + '  |  UPI: ' + RUPEE + upiVal.toFixed(2);
            } else if (methods.cash) {
                detail = 'Paid via Cash';
            } else {
                detail = 'Paid via UPI';
            }
            document.getElementById('success-detail').innerText = detail;
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
            }, 2500);
        }"""

new_confirm = """        function confirmPayment() {
            let total = getTotal();
            let cashVal = parseFloat(document.getElementById('input-cash').value) || 0;
            let upiVal = parseFloat(document.getElementById('input-upi').value) || 0;

            let payMethod = 'cash';
            if (methods.cash && methods.upi) payMethod = 'split';
            else if (methods.upi) payMethod = 'upi';

            // Build items array from cart
            let orderItems = [];
            for (let id in cart) {
                orderItems.push({ id: id, qty: cart[id].qty });
            }

            // Save order to database
            fetch('/api/create-order/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    items: orderItems,
                    payment_method: payMethod,
                    cash_amount: cashVal,
                    upi_amount: upiVal,
                    total: total
                })
            })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                closePayment();

                let orderNum = data.order_number || '';
                document.getElementById('success-amount').innerText = RUPEE + total.toFixed(2);
                let detail = 'Order #' + orderNum + '\\n';
                if (methods.cash && methods.upi) {
                    detail += 'Cash: ' + RUPEE + cashVal.toFixed(2) + '  |  UPI: ' + RUPEE + upiVal.toFixed(2);
                } else if (methods.cash) {
                    detail += 'Paid via Cash';
                } else {
                    detail += 'Paid via UPI';
                }
                document.getElementById('success-detail').innerText = detail;
                document.getElementById('success-overlay').classList.add('active');

                // Show bill button
                let billLink = document.getElementById('bill-link');
                if (billLink && orderNum) {
                    billLink.href = '/bill/' + orderNum + '/';
                    billLink.style.display = 'inline-block';
                }

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
                    if (billLink) billLink.style.display = 'none';
                    cart = {};
                    updateCartUI();
                }, 3500);
            });
        }"""

c = c.replace(old_confirm, new_confirm)

# Add bill link to success overlay
c = c.replace(
    '<div class="success-detail" id="success-detail"></div>',
    '<div class="success-detail" id="success-detail"></div>\n        <a id="bill-link" href="#" target="_blank" style="display:none; margin-top:20px; padding:12px 30px; background:white; color:#4ECB71; border-radius:8px; font-weight:800; text-decoration:none; font-size:1rem;">View Bill</a>'
)

# Add admin links for Orders and Sales in header
old_admin_links = """{% if request.user.profile.role == 'admin' %}
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:20px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Manage Menu</a>
            {% endif %}"""

new_admin_links = """{% if request.user.profile.role == 'admin' %}
            <a href='/users/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Staff</a>
            <a href='/menu/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Menu</a>
            <a href='/orders/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Orders</a>
            <a href='/sales/' style='color:inherit;text-decoration:none;margin-right:15px;padding:8px 12px;border:2px solid var(--border);border-radius:8px;transition:0.2s' onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">Sales</a>
            {% endif %}"""

c = c.replace(old_admin_links, new_admin_links)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
