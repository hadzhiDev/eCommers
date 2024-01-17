from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.conf import settings

from account.managers import UserManager
from utils.models import TimeStampAbstractModel


class User(AbstractUser, TimeStampAbstractModel):

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='avatars/',
                               force_format='WEBP', quality=90, verbose_name='аватарка',
                               null=True, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона', blank=True, null=True)
    email = models.EmailField(verbose_name='электронная почта', unique=True, blank=True, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = 'полное имя'

    def __str__(self):
        return f'{self.get_full_name or str(self.email)}'


def get_expire_date():
    return timezone.now() + timezone.timedelta(days=1)


class UserResetPassword(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'Ключ для сброса пароля'
        verbose_name_plural = 'Ключи для сброса пароля'
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name='пользователь')
    key = models.UUIDField('ключ', default=uuid4, editable=False, unique=True)
    expire_date = models.DateTimeField('срок действия', default=get_expire_date)

    def __str__(self):
        return f'{self.user}'

    def is_expired(self):
        return timezone.now() > self.expire_date
