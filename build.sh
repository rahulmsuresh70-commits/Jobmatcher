#!/usr/bin/env bash
set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('ADMIN_USERNAME')
email = os.environ.get('ADMIN_EMAIL', '')
password = os.environ.get('ADMIN_PASSWORD')

if username and password:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_staff': True,
            'is_superuser': True,
        }
    )

    if created:
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print('Admin user created successfully.')
    else:
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print('Admin user updated successfully.')
"