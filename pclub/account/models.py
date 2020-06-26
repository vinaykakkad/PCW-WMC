from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


# Account Manger for custom user model
class AccountManager(BaseUserManager):
    """
        User Manager for custom user model
    """

    def create_user(self, username, email, password=None, fullname=None, 
                    cf_username=None, github_username=None, is_active=True, 
                    is_staff=False, is_superuser=False, is_activated=False):
        if not username:
            raise ValueError('Users must have a unique username.')
        if not email:
            raise ValueError('Users must have an email.')
        if not password:
            raise ValueError('Users must have a password.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            fullname=fullname,
            cf_username=cf_username,
            github_username=github_username
        )

        user.set_password(password)
        user.is_active = is_active
        user.staff = is_staff
        user.is_superuser = is_superuser
        user.is_activated = is_activated
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
            is_staff=True,
            is_activated=True
        )
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_activated=True
        )
        return user


class Account(AbstractBaseUser):
    """
        Custom user Model
    """
    
    # custom fields
    username = models.CharField(unique=True, max_length=220)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=220, blank=True, null=True)
    cf_username = models.CharField(max_length=220, blank=True, null=True)
    github_username = models.CharField(max_length=220, blank=True, null=True)
    # required fields
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)

    # this is the field that will be asked during authentication
    USERNAME_FIELD = 'username'
    # required fields other than password and USERNAME_FIELD
    REQUIRED_FIELDS = ['email', ]
    # custom fields not included in required field should have null = True

    objects = AccountManager()

    # required methods if we want to access user using admin
    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.staff

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # We can add custom methods as per requirements
