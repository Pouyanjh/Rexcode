from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class Usermanager(UserManager):
    def _create_user(self, username, email, password, fullname, **extra_fields):
        if not email:
            raise ValueError('you must set valid mail')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            fullname=fullname,
            extra_fields=extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username=None, email=None, password=None, fullname=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, fullname, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class user(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=200, blank=True, unique=True)
    email = models.EmailField(unique=True, blank=True)
    fullname = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    activation_key = models.CharField(max_length=36, blank=True)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'password', 'fullname']

    USERNAME_FIELD = 'username'

    class meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'