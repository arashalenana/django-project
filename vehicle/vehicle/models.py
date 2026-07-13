from django.db import models

# Create your models here.
class Vehicle(models.Model):
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    year=models.IntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name