from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    phone = PhoneNumberField(blank=True)
    favorites = models.ManyToManyField("self", blank=True, null=True, symmetrical=False)

    def __str__(self):
        return f"{self.external_id} {self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
