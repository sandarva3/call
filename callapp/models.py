from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField()


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    questionNo = models.IntegerField()
    questionText = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Userdata of {self.user.username}"