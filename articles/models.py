from django.db import models
from django.db.models.signals import pre_save, post_delete
from uuid import uuid4
import os
from django.utils.text import slugify
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class ArticleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=60, null=False)
    description = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True)
    content = models.TextField(null=False)
    slug = models.SlugField(default='', blank=True)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_title = slugify(self.title)
            self.slug = f'{slug_title}-{self.id}'

        super().save(*args, **kwargs)


@receiver(pre_save, sender=ArticleModel)
def delete_old_image(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = ArticleModel.objects.get(id=instance.id)
        except ArticleModel.DoesNotExist:
            return
        if old_instance.image:
            old_image_path = os.path.join(
                settings.MEDIA_ROOT, str(old_instance.image))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)


@receiver(post_delete, sender=ArticleModel)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.exists(image_path):
            os.remove(image_path)


