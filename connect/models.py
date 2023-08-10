from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='received_requests')

    def __str__(self):
        return self.sender.username

class Connection(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_connections')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='friend_connections')

    def __str__(self):
        return self.user.username