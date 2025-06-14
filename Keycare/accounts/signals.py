from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

@receiver(post_migrate)
def create_staff_user(sender, **kwargs):
    """
    This signal is triggered after migrations are applied. 
    It ensures that a default admin user (staff user) is created 
    if it doesn't already exist.
    """
    User = get_user_model()  # This will dynamically fetch the custom user model
    
    # Check if the 'admin' user already exists
    if not User.objects.filter(username='admin').exists():
        try:
            # Create the admin user
            staff_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',  # Replace with actual email
                password='securepassword',  # Replace with a secure password
                is_staff=True,               # Grant staff status
                is_superuser=True            # Grant superuser status
            )

            # Assign permissions for adding, changing, and deleting users
            try:
                user_ct = ContentType.objects.get_for_model(User)  # Dynamically fetch the ContentType for User model
                perms = Permission.objects.filter(
                    content_type=user_ct,
                    codename__in=['add_user', 'change_user', 'delete_user']
                )
                staff_user.user_permissions.set(perms)  # Assign permissions to the user
            except ContentType.DoesNotExist:
                print(f"ContentType for '{User.__name__}' not found, skipping permissions assignment.")

            # Save the user with the assigned permissions
            staff_user.save()
            print("Staff user 'admin' created successfully.")
        
        except IntegrityError as e:
            print(f"Error creating staff user: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

