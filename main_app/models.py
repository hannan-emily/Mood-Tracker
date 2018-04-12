from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) #added to create 1:M relationship
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Toy(models.Model):
	name = models.CharField(max_length=100)
	cats = models.ManyToManyField(Cat)

	def __str__(self):
		return self.name

class Picture(models.Model):
    name = models.TextField()
    mood = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)






