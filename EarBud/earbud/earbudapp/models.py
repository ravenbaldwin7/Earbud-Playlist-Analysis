from django.db import models

class EarBudMod(models.Model) :
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
# Create your models here.
