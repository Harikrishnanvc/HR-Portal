from django.contrib.auth.models import User
from django.db import models
from admin_panel.models import AdminUser


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=AdminUser, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username