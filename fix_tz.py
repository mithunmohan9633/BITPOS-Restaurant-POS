# Fix 2: Update timezone to India
settings_path = 'restaurant_pos/settings.py'
with open(settings_path, 'r', encoding='utf-8') as f:
    s = f.read()

s = s.replace("TIME_ZONE = 'UTC'", "TIME_ZONE = 'Asia/Kolkata'")

if "USE_TZ = True" in s:
    s = s.replace("USE_TZ = True", "USE_TZ = True")

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(s)
print("Timezone updated to Asia/Kolkata")
