from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):

    def user_icon_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<username>/icons/<filename>
        return 'user_{0}/icons/{1}'.format(instance.user.username, filename)

    GENDERS = (("M", "Male"), ("F", "Female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=16, choices=GENDERS, default="M")
    nickname = models.CharField(max_length=32)
    icon = models.ImageField(
        upload_to=user_icon_path,
        default="default_pictures/male-default.png"
    )

    def __str__(self):
        return self.user.username
