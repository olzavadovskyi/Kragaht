
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts:category_posts', kwargs={'category_slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = RichTextField()  # CKEditor
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    time_create = models.DateTimeField(auto_now=True)
    time_update = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_slug': self.slug})

    def can_edit_or_delete(self, user):
        return user == self.author or user.is_staff

    def get_like_count(self):
        return self.likes.count()

    def user_liked(self, user):
        return self.likes.filter(id=user.id).exists()

