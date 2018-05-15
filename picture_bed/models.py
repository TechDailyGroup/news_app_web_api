from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_id/filename
        return 'user_{0}/pictures/{1}'.format(instance.user.id, filename)
    
    picture = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.picture.url
