from django.db import models
from django.contrib.auth.models import User



class Picture(models.Model):
    name = models.TextField()
    mood = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)






