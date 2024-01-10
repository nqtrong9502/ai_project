from django.db import models
class person(models.Model):
  id_person = models.AutoField(primary_key=True)
  name = models.TextField()

# Create your models here.
