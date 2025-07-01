from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import get_language as _
from accounts.managers import UserManager
from accounts.utils.image_upload import USER_DIRECTORY_PATH
from accounts.utils.gender import GENDERS
from accounts.utils.role import ROLES
from accounts.utils.account_type import ACCOUNT_TYPES
from accounts.services.user_id import GENERATE_USER_ID
from core.utils import VALIDATE_EMAIL, VALIDATE_PHONE_NUMBER, VALIDATE_IMAGE_SIZE, VALIDATE_IMAGE_EXTENSION, GENERATE_SLUG

User = get_user_model()

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    image = models.ImageField(
        upload_to=USER_DIRECTORY_PATH,
        validators=[VALIDATE_IMAGE_EXTENSION, VALIDATE_IMAGE_SIZE],
        verbose_name=_('Image'),
        help_text=_('Upload your image...'),
    )
    user_id = models.PositiveIntegerField(
        unique=True,
        db_index=True,
        max_length=9,
        validators=[MinLengthValidator(9)],
        editable=False,
        verbose_name=_('User ID'),
    )
    username = models.CharField(
        unique=True,
        db_index=True,
        max_length=40,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message=_('Username can only contain letters, numbers, and underscores.'),
            ),
        ],
        verbose_name=_('Username'),
        help_text=_('Enter your username...'),
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        editable=False,
    )
    name = models.CharField(
        max_length=60,
        validators=[MinLengthValidator(3)],
        verbose_name=_('Name'),
        help_text=_('Enter your name...'),
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        max_length=80,
        validators=[VALIDATE_EMAIL, MinLengthValidator(10)],
        verbose_name=_('Email'),
        help_text=_('Enter your email...'),
    )
    number = models.CharField(
        unique=True,
        db_index=True,
        max_length=20,
        validators=[VALIDATE_PHONE_NUMBER, MinLengthValidator(5)],
        verbose_name=_('Number'),
        help_text=_('Enter your number...'),
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDERS,
        verbose_name=_('Gender'),
        help_text=_('Enter your gender...'),
    )
    birth_date = models.DateField(
        verbose_name=_('Birth Date'),
        help_text=_('Enter your birth date...'),
    )
    country = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(3)],
        verbose_name=_('Country'),
        help_text=_('Enter your country')
    )
    signature = models.CharField(
        max_length=40,
        validators=[MinLengthValidator(3)],
        verbose_name=_('Signature'),
        help_text=_('Enter your signature...'),
    )
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        verbose_name=_('Account Type'),
        help_text=_('Enter your account type...'),
    )
    role = models.CharField(
        default=20,
        choices=ROLES,
        verbose_name=_('Role'),
        help_text=_('Enter your role...'),
    )

    terms_accepted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username or self.email
    
    def clean(self):
        if self.role == 'admin':
            existing_admin = User.objects.filter(role='admin')
            if self.pk:
                existing_admin = existing_admin.exclude(pk=self.pk)
            if existing_admin.exists():
                raise DjangoValidationError(_('Only one admin is allowed.'))
            
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = GENERATE_USER_ID(self.role)
        if self.pk:
            orig = User.objects.only("username").filter(pk=self.pk).first()
            if orig and orig.username != self.username:
                self.slug = GENERATE_SLUG(self.username)
        else:
            self.slug = GENERATE_SLUG(self.username)

        super().save(*args, **kwargs)
            
    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)

class ActiveSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='active_session')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"
    