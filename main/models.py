from django.db import models

from account.models import Account

class Section(models.Model):

    def section_icon_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/section_<section_name>/icons/<filename>
        return 'section_{0}/icons/{1}'.format(instance.name, filename)
    
    creator = models.ForeignKey(Account, related_name="created_sections", on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)
    subscribers = models.ManyToManyField(Account, related_name="subscribed_sections")
    icon = models.ImageField(
        upload_to = section_icon_path,
        default = "default_pictures/section_default.png"
    )

    def __str__(self):
        return self.name

class Article(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    publish_time = models.DateTimeField(auto_now_add=True, db_index=True)
    image1_url = models.CharField(max_length=160, null=True)
    image2_url = models.CharField(max_length=160, null=True)
    image3_url = models.CharField(max_length=160, null=True)
    # json format 
    # [
    #   {'type': <str, 'text'/'image'>, 
    #    'content': <str, text or image url>},
    #   ...
    # ]
    content = models.TextField()

    def __str__(self):
        return "{section} {title}".format(section=self.section.name, title=self.title)

""" TODO
class Actions(models.Model):
    ACTION_TYPES = (('visit_page', 'visit_page'), )

    user = models.ForeignKey(Account)
    type = models.CharField(max_length='32', choices=ACTION_TYPES)
    value = models.CharField(max_length = '256')
"""
