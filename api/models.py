from django.db import models

class ErrorReport(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"Error {self.code}"