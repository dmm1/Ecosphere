from django.db import models
import uuid


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bid = models.IntegerField(default=00000)
    name = models.CharField(max_length=100)
    date_of_creation = models.DateField()
    Potential = models.IntegerField()




# Create your models here.
