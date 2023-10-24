from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta: 
        ordering = ['-updated', '-created'] # Domyślne Order BY w klasie, pierwszy ma priorytet, opcjonalnie drugi 


    def __str__(self):
        return str(self.name)
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # Zapis oznacza to, że gdy Room zostanie usuniety to to też zostanie|SET_NULL zamiast usunięcia zostanie dane NULL
    body = models.TextField()
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]