import os

# Create teacher dashboard by cloning student dashboard
with open(r'c:\Users\dell\school-django\school\templates\students\student-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Student Dashboard', 'Teacher Dashboard')
content = content.replace('Welcome Bruklin!', 'Welcome Teacher!')

with open(r'c:\Users\dell\school-django\school\templates\teachers\teacher-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
