from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_count = models.ManyToManyField("User", related_name="likes", blank=True)

    def __str__(self):
        return f"{self.user} on {self.timestamp} wrote \"{self.body}\""

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp,
        }
    

    