import os
import sys

# set up Django environment
sys.path.append(r'C:\Users\Дарій\Desktop\проект\New Web')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

import django
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='testuser').exists():
    User.objects.create_superuser('testuser', 'test@example.com', 'password123')
    print('superuser created')
else:
    print('superuser already exists')
