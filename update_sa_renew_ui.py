path = 'core/templates/core/super_admin.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add Renew button to Action column
old_action_cell = """                    <td>
                        <a href="/super-admin/toggle-company/{{ comp.id }}/" class="toggle-btn {% if comp.is_active %}toggle-block{% else %}toggle-unblock{% endif %}">
                            {% if comp.is_active %}Block{% else %}Unblock{% endif %}
                        </a>
                    </td>"""

new_action_cell = """                    <td>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <a href="/super-admin/toggle-company/{{ comp.id }}/" class="toggle-btn {% if comp.is_active %}toggle-block{% else %}toggle-unblock{% endif %}" style="flex: 1; text-align: center;">
                                {% if comp.is_active %}Block{% else %}Unblock{% endif %}
                            </a>
                            <button onclick="toggleRenew('{{ comp.id }}')" class="toggle-btn" style="background: rgba(255, 215, 0, 0.15); color: #FFD700; flex: 1;">Renew</button>
                        </div>
                    </td>"""

c = c.replace(old_action_cell, new_action_cell)

# Add a hidden renewal row after each company row
row_pattern = "</tr>"
replacement = """</tr>
                <tr id="renew-row-{{ comp.id }}" style="display: none; background: rgba(255, 215, 0, 0.05);">
                    <td colspan="6">
                        <form method="POST" action="/super-admin/renew-company/{{ comp.id }}/" style="display: flex; gap: 15px; align-items: center; padding: 10px;">
                            {% csrf_token %}
                            <div style="flex: 1;">
                                <label style="font-size: 0.7rem; color: var(--muted); margin-bottom: 2px; display: block;">Update Plan</label>
                                <select name="plan_name" style="margin: 0; padding: 8px;">
                                    <option value="Basic" {% if comp.plan_name == 'Basic' %}selected{% endif %}>Basic</option>
                                    <option value="Standard" {% if comp.plan_name == 'Standard' %}selected{% endif %}>Standard</option>
                                    <option value="Premium" {% if comp.plan_name == 'Premium' %}selected{% endif %}>Premium</option>
                                </select>
                            </div>
                            <div style="flex: 1;">
                                <label style="font-size: 0.7rem; color: var(--muted); margin-bottom: 2px; display: block;">New Expiry Date</label>
                                <input type="date" name="valid_until" value="{{ comp.valid_until|date:'Y-m-d' }}" style="margin: 0; padding: 8px;" required>
                            </div>
                            <button type="submit" class="toggle-btn" style="background: #FFD700; color: #1A1A2E; padding: 10px 20px; border-radius: 8px; font-weight: 800; margin-top: 15px;">Save Renewal</button>
                            <button type="button" onclick="toggleRenew('{{ comp.id }}')" class="toggle-btn" style="background: transparent; color: var(--muted); border: 1px solid var(--border); margin-top: 15px;">Cancel</button>
                        </form>
                    </td>
                </tr>"""

# Need to be careful with replace if </tr> is common. But it should be fine here as I'm replacing within the loop context.
# Actually let's use a more specific target.
c = c.replace(new_action_cell + "\n                </tr>", new_action_cell + "\n                " + replacement)

# Add the JS function to toggle the row
js_script = """
    <script>
        function toggleRenew(id) {
            const row = document.getElementById('renew-row-' + id);
            if (row.style.display === 'none') {
                row.style.display = 'table-row';
            } else {
                row.style.display = 'none';
            }
        }
    </script>
</body>"""

c = c.replace("</body>", js_script)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated super_admin.html with renewal forms")
