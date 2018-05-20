from django.db import models

from main.models import Article

class ArticleTags(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="article_tags")
    level1_tag = models.CharField(max_length=64)
    level2_tag = models.CharField(max_length=64)
    level3_tag = models.CharField(max_length=64)
