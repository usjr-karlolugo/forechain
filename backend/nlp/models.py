from django.db import models


class Alert(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    sentiment = models.CharField(max_length=50)
    sentiment_score = models.FloatField()
    topic = models.CharField(max_length=100)
    score = models.JSONField()  # To store the array of scores
    entities = models.JSONField()  # To store locations and companies as JSON
    summary = models.TextField()
    image_url = models.URLField()
    
    def __str__(self):
        return self.title
