"""
 user models.
 AbstractBaseUser class is used for authentication.
# BaseUserManager class is used to create user objects. 
# PermissionsMixin class is used to add permissions to the user model.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    ''' Manager for user.'''
    
    def create_user(self,username, email, password=None, **extra_fields):
        ''''create, save and return a new user.'''
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email,password=None):
        '''create and return a superuser with given email and password.'''
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user in the system.'''
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    #profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
