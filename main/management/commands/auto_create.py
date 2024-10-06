import json
from django.core.management.base import BaseCommand
from main.models import User
import random
import calendar

def generate_random_date():
    year = random.randint(2000, 2022)
    month = random.randint(1, 12)
    days_in_month = calendar.monthrange(year, month)[1]
    day = random.randint(1, days_in_month)
    formatted_date = f"{year}-{month:02d}-{day:02d}"
    return formatted_date

class Command(BaseCommand):
    help = 'Create users from users.json file'

    def handle(self, *args, **kwargs):
        with open('tests/users.json') as f:
            data = json.load(f)

        for user_data in data:
            username = user_data['username']
            email = user_data['email']
            designation = user_data['designation']
            is_otp_req = user_data['is_otp_req']
            password = user_data['password']
            confirm_password = password
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                designation=designation,
                is_otp_req=bool(is_otp_req),
                date_of_joining=generate_random_date(),
                is_employee=True,
                confirm_password=confirm_password
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
            self.stdout.write(f'Password: {password}')
