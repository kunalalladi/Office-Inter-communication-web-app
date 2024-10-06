from django.core.management.base import BaseCommand
from getpass import getpass
from ...models import User

class Command(BaseCommand):
    help = 'Create an admin user with additional fields'

    def handle(self, *args, **options):
        username = input("Username: ")
        email = input("Email: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = getpass("Password: ")
        confirm_password = getpass("Confirm Password: ")

        while password != confirm_password:
            print("Passwords do not match.")
            password = getpass("Password: ")
            confirm_password = getpass("Confirm Password: ")

        user = User.objects.create_superuser(username=username, password=password, email=email,first_name=first_name, last_name=last_name)
        self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))

