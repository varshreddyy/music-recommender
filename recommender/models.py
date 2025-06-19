from django.db import models

class Song(models.Model):
    artist = models.CharField(max_length=255)
    song = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"{self.song} by {self.artist}"
