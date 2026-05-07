path = 'core/templates/core/super_admin.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Update stats row to include Global Revenue
old_stats = """        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">Total Companies</div>
                <div class="stat-value">{{ companies|length }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Active Companies</div>
                <div class="stat-value" style="color: var(--success)">{{ active_count }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Store Admins</div>
                <div class="stat-value" style="color: var(--accent)">{{ admins|length }}</div>
            </div>
        </div>"""

new_stats = """        <div class="stats-row" style="grid-template-columns: repeat(4, 1fr);">
            <div class="stat-card">
                <div class="stat-label">Total Companies</div>
                <div class="stat-value">{{ companies|length }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Active Companies</div>
                <div class="stat-value" style="color: var(--success)">{{ active_count }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Store Admins</div>
                <div class="stat-value" style="color: var(--accent)">{{ admins|length }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Global Revenue</div>
                <div class="stat-value" style="color: #FFD700">&#8377;{{ global_revenue }}</div>
            </div>
        </div>"""

c = c.replace(old_stats, new_stats)

# Update form to include validity and plan
old_form = """                    <select name="pos_type">
                        <option value="restaurant">Restaurant POS</option>
                        <option value="retail">Retail POS</option>
                    </select>
                    <button type="submit" class="btn btn-primary">Register Company</button>"""

new_form = """                    <div style="display: flex; gap: 10px;">
                        <select name="pos_type" style="flex: 1;">
                            <option value="restaurant">Restaurant POS</option>
                            <option value="retail">Retail POS</option>
                        </select>
                        <select name="plan_name" style="flex: 1;">
                            <option value="Basic">Basic Plan</option>
                            <option value="Standard" selected>Standard Plan</option>
                            <option value="Premium">Premium Plan</option>
                        </select>
                    </div>
                    <div style="margin-top: 10px;">
                        <label style="font-size: 0.8rem; color: var(--muted); display: block; margin-bottom: 5px;">Valid Until</label>
                        <input type="date" name="valid_until" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Register Company</button>"""

c = c.replace(old_form, new_form)

# Update company table headers and data
old_table_headers = """                <tr>
                    <th>Company Name</th>
                    <th>POS Type</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>"""

new_table_headers = """                <tr>
                    <th>Company Name</th>
                    <th>POS Type</th>
                    <th>Plan</th>
                    <th>Expiry Date</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>"""

c = c.replace(old_table_headers, new_table_headers)

old_table_data = """                {% for comp in companies %}
                <tr>
                    <td style="font-weight: 800">{{ comp.name }}</td>
                    <td>
                        <span class="type-badge {% if comp.pos_type == 'restaurant' %}type-restaurant{% else %}type-retail{% endif %}">
                            {{ comp.get_pos_type_display }}
                        </span>
                    </td>
                    <td style="color: var(--muted)">{{ comp.address|default:"--" }}</td>
                    <td>
                        {% if comp.is_active %}
                        <span class="status-active">Active</span>
                        {% else %}
                        <span class="status-blocked">Blocked</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="/super-admin/toggle-company/{{ comp.id }}/" class="toggle-btn {% if comp.is_active %}toggle-block{% else %}toggle-unblock{% endif %}">
                            {% if comp.is_active %}Block{% else %}Unblock{% endif %}
                        </a>
                    </td>
                </tr>"""

new_table_data = """                {% for comp in companies %}
                <tr>
                    <td style="font-weight: 800">{{ comp.name }}</td>
                    <td>
                        <span class="type-badge {% if comp.pos_type == 'restaurant' %}type-restaurant{% else %}type-retail{% endif %}">
                            {{ comp.get_pos_type_display }}
                        </span>
                    </td>
                    <td style="font-weight: 600; color: var(--primary)">{{ comp.plan_name }}</td>
                    <td style="color: var(--text)">{{ comp.valid_until|date:"d M Y"|default:"No Date" }}</td>
                    <td>
                        {% if comp.is_active %}
                        <span class="status-active">Active</span>
                        {% else %}
                        <span class="status-blocked">Blocked</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="/super-admin/toggle-company/{{ comp.id }}/" class="toggle-btn {% if comp.is_active %}toggle-block{% else %}toggle-unblock{% endif %}">
                            {% if comp.is_active %}Block{% else %}Unblock{% endif %}
                        </a>
                    </td>
                </tr>"""

c = c.replace(old_table_data, new_table_data)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated super_admin.html")
