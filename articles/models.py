from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Article(models.Model):
    """
    Model to hold data about articles
    """
    title = models.CharField(max_length=40)
    headline = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.id})
