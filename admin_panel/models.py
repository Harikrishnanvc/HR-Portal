from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

class AdminUser(AbstractUser):
    object = User()
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, null=True, unique=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True,)
    employee_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, null=True)
    mobile_no = models.IntegerField(null=True)
    department = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(upload_to='images', null=True)
    password = models.CharField(max_length=100, null=True)
    is_superuser = models.BooleanField(null=True,default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_absolute_url(self):
        return f"admin_user/{self.first_name}"

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "AdminUser"


class FakeAddress(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class Product(models.Model):
    title = models.CharField(max_length=50)

    def get_absolute_url(self):
        return f"products/{self.title}"

    def __str__(self):
        return self.title



