from django.db import models
from django.contrib.auth.models import User
from  datetime import datetime


class Stone(models.Model):
    stone_name = models.CharField(max_length=255)

    def __str__(self):
        return self.stone_name

class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    power_duration = models.PositiveIntegerField()  # Duration in seconds

    def __str__(self):
        return f"{self.user.username}'s activation of {self.stone.stone_name}"

    def is_active(self):
        now = datetime.now()
        return self.start_time <= now <= self.end_time if self.start_time and self.end_time else False
