from django.db import models

# Create your models here.
from user.models import User


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    hit = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return f'Board({self.board_id}, {self.title}, {self.content}, {self.hit}, {self.regdate}, {self.groupno}, {self.orderno}, {self.depth}, {self.user})'