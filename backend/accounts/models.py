from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User model """

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    id = models.BigAutoField(primary_key=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, null=True, verbose_name='First name')
    last_name = models.CharField(max_length=100, null=True, verbose_name='Last name')
    is_active = models.BooleanField(default=False, verbose_name='Is active?')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Last login')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['id']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class UserSettings(models.Model):
    """ User settings model """

    id = models.BigAutoField(primary_key=True, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    general_instructions = models.TextField(null=True, blank=True, verbose_name='General instructions')
    terminology = models.TextField(null=True, blank=True, verbose_name='Terminology')
    template_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Template name')
    project_instructions = models.TextField(null=True, blank=True, verbose_name='Project instructions')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    template_content = models.BinaryField(null=True, blank=True, verbose_name='Template content')

    class Meta:
        db_table = 'users_settings'
        ordering = ['id']

    def __str__(self):
        return f'{self.user.get_full_name()} settings'
