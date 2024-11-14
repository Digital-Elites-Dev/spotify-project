# music/models.py
from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Track(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="tracks")
    name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255, unique=True)
    energy = models.FloatField(null=True)
    loudness = models.FloatField(null=True)
    key = models.IntegerField(null=True)
    
    tempo = models.FloatField(null=True)
    danceability = models.FloatField()  # Add this field if it doesn't exist

    # class Meta:
    #     unique_together = ['spotify_id', 'playlist']  # Ensure spotify_id is unique per playlist

    def __str__(self):
        return self.name


