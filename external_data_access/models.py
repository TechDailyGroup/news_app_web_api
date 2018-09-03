from django.db import models

from main.models import Article

class ArticleText(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="article_text")
    text = models.TextField()
