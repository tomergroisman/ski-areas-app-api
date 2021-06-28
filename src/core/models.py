
from django.db import models
from django.contrib.auth.models import (
  BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from core.services.translation import i18n


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(
        self,
        username=None,
        password=None,
        email=None,
        **extra_fields
    ):
        """Create a new user"""
        if not username:
            raise ValueError(i18n('CREATE_USER_NO_USERNAME'))

        if not email:
            raise ValueError(i18n('CREATE_USER_NO_EMAIL'))

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, **params):
        """Create a new super user"""
        user = self.create_user(**params)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    username = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )
    email = models.EmailField(
        max_length=255, unique=True, null=False, blank=False
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(
        i18n('ADMIN_USER_ACTIVE'),
        help_text=i18n('ADMIN_USER_ACTIVE_HELPER_TEXT'),
        default=True,
    )
    is_staff = models.BooleanField(
        i18n('ADMIN_USER_STAFF_STATUS'),
        help_text=i18n('ADMIN_USER_STAFF_STATUS_HELPER_TEXT'),
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
