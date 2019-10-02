from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Poster(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Permissive_to_post = models.BooleanField(default=False)

    def __str__(self):
        if self.Permissive_to_post:
            return f'{self.user.username} is a Poster'
        else:
            return f'{self.user.username} Can be a poster'

    def save(self, *args, **kwargs):
        super(Poster, self).save(*args, **kwargs)