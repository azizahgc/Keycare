from django.core.management.base import BaseCommand
from accounts.models import CustomUser  # Import the CustomUser model

class Command(BaseCommand):
    help = 'Hashes the passwords for all users'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()  # Get all users
        count = 0  # Keep track of how many passwords are hashed

        for user in users:
            if not user.password.startswith('pbkdf2_sha256$'):  # Check if password is already hashed
                user.set_password(user.password)  # Hash the plain-text password
                user.save()  # Save the user with the hashed password
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Password for {user.username} has been hashed."))  # Log success
            else:
                self.stdout.write(self.style.SUCCESS(f"User {user.username} already has a hashed password."))  # Log if already hashed

        self.stdout.write(self.style.SUCCESS(f'Passwords hashed for {count} users.'))
