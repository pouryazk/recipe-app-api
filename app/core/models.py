import uuid
import os
from django.db import models
""" extended line with backslash """
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings  # recommanded way to retrieve django settings

def recipe_image_file_path(instance, filename):
    """ generate file path for new recipe image """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


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


class Ingredient(models.Model):
    """ ingredient to be used in a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ recipe objects """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # allowing Null value is not recommanded
    ingredients = models.ManyToManyField('Ingredient')
    # if you remove the string, you have to make sure ingredient is above recipe
    tags = models.ManyToManyField('Tag')
    # read the docs of ManyToManyField
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
