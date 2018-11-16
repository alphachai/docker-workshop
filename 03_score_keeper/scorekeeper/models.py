from django.db import models

class Score(models.Model):
    player_one = models.CharField(max_length=30)
    player_two = models.CharField(max_length=30)
    score_one = models.IntegerField()
    score_two = models.IntegerField()
