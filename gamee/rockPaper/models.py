from django.db import models


# Create your models here.
class UserGame(models.Model):
    username = models.CharField(max_length=100)
    room_id = models.IntegerField(null=True)
    select_el = models.IntegerField(null=True)

