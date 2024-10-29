from django.db import models

# Create your models here.
from django.db import models

class Task(models.Model):
    description = models.CharField(max_length=4096)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description