# Step 1: Update Company model with validity and plan fields
path = 'core/models.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

if 'valid_until' not in c:
    import_line = "class Company(models.Model):"
    new_fields = """class Company(models.Model):
    plan_name = models.CharField(max_length=50, default='Standard')
    valid_until = models.DateField(null=True, blank=True)"""
    c = c.replace(import_line, new_fields)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated models.py")
