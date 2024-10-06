from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from ...models import User

import random
import calendar

def generate_random_date():
    # Generate a random year between 2000 and 2022
    year = random.randint(2000, 2022)

    # Generate a random month (1 to 12)
    month = random.randint(1, 12)

    # Get the number of days in the selected month and year
    days_in_month = calendar.monthrange(year, month)[1]

    # Generate a random day (1 to the number of days in the selected month)
    day = random.randint(1, days_in_month)

    # Format the date as "Year, Month, Date"
    formatted_date = f"{year}-{month:02d}-{day:02d}"
    return formatted_date


class Command(BaseCommand):
    help = 'Create a new user with random username and password.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Specifies the username for the new user.')
        parser.add_argument('email', type=str, help='Specifies the email for the new user.')
        parser.add_argument('password', type=str, help="Specifies the password for the new user.")
        parser.add_argument('designation', type=str, help='Specifies the designation for the new user.')
        parser.add_argument('is_otp_req', type=str, help="Whether the OTP is required")
        
    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        designation = kwargs['designation']
        is_otp_req = kwargs['is_otp_req']
        
        if designation not in ["employee", "officer", "chief officer"]:
            raise Exception("Designation doesn't match")
        if designation == "employee": is_employee=1
        else: is_employee=0

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            confirm_password=password,
            designation=designation,
            is_otp_req=is_otp_req,
            date_of_joining=generate_random_date(),
            is_employee=is_employee
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
        self.stdout.write(f'Password: {password}')
