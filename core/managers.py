from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    # Custom user manager that uses email as unique identifier for auth instead of username

    def create_user(self, email, password, **extra_fields):
        # Create and save user given email and password
        if not email:
            raise ValueError(_('You must enter your email'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save superuser given email and password
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Admin must have is_admin=True'))

        return self.create_user(email, password, **extra_fields)