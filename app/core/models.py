from django.db import models
""" extended line with backslash """
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings  # recommanded way to retrieve django settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and Saves a new User """
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # model is the user model
        user.set_password(password)
        user.save(using=self._db)

        return user  # returns the user model

    def create_superuser(self, email, password):
        """ creates and save a new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        """ we need to save because we modified it """
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User model that supports using email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # must set the default to True
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # remember to include () at the end
    USERNAME_FIELD = 'email'  # set this as a string


class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
