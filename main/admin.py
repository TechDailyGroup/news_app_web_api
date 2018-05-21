from django.contrib import admin

from main.models import Section, Article

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'description')
    list_filter = ('creator__user__username', )
    search_fields = ('creator__user__username', 'name')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'publish_time')
    list_filter = ('section__name', )
    search_fields = ('title', 'section__name')

admin.site.register(Section, SectionAdmin)
admin.site.register(Article, ArticleAdmin)
