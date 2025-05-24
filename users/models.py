from django.db import models

# Create your models here.

class UserProfile(models.Model):
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    picture_thumbnail = models.URLField()
    uuid = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
