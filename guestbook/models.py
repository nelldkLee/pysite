from django.db import models

# Create your models here.
class GuestBook(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    contents = models.TextField()
    joindate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'GuestBook({self.name}, {self.contents}, {self.joindate})'