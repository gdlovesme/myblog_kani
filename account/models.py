from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


#TODO: create activation_code

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    # защищенный метод _create_user
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email) #normalise email проверяет использует ли собачку и тд
        user = self.model(email=email) #создаем обьект юзера и указываем его параметры (создаем от модели)
        user.set_password(password) #метод set password сохраняет пароль в хэшированном виде
        # user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)  # normalise email проверяет использует ли собачку и тд
        user = self.model(email=email)  # создаем обьект юзера и указываем его параметры (создаем от модели)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractUser):
    username = None #чтобы его не было
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False) #станет True, только когда пользователь активируется
    activation_code = models.CharField(max_length=50, blank=True) #blank True тк поле будет заполненым до того как юзер активирует себя, но после активации поле надо опустошить

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()#менеджер objects это наш кастомный Myusermanager

    def __str__(self):
        return self.email #при вызове объекта будет возвращаться email


