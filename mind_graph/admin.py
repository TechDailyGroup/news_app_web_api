from django.contrib import admin

from mind_graph.models import ArticleTags

class ArticleTagsAdmin(admin.ModelAdmin):
    list_display = ('article', 'level1_tag', 'level2_tag', 'level3_tag')
    search_fields = ('article__title', )

admin.site.register(ArticleTags, ArticleTagsAdmin)
