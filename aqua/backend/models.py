# models.py

from django.db import models

class ImageData(models.Model):
    arduino_id = models.CharField(max_length=20)
    image_path = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    sensor1 = models.IntegerField()
    sensor2 = models.IntegerField()

    def __str__(self):
        return self.image_path
    

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name

