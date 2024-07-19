from django.db import models

# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self) :
        return self.name


"""
1 - create database model (roomMember) | Store user name, uid and
2 - On Join, create RoomMember in database
3 - on handleUserJoin event, query db for room member name by uid
4 - on leave, delete RoomMember
"""
