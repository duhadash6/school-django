import os

files = ['c:/Users/dell/school-django/school/faculty/views.py', 'c:/Users/dell/school-django/school/student/views.py']

for f_path in files:
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace("\\'", "'")
    
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)
