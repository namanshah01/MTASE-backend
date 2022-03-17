from django.db import models

# Create your models here.

class File(models.Model):
    name  = models.CharField(max_length=100)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.timestamp}"


class Text(models.Model):
    text = models.TextField(blank=False)
    # translatedText = models.TextField(blank=True)
    # title = models.TextField(blank=False)
    # summary = models.TextField(blank=False)
    # textLength = models.IntegerField()
    # summaryLength = models.IntegerField()
    # original_language = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.text}-{self.timestamp}"