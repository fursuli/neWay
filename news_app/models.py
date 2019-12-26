from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'moderation')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('related_post', 'text', 'author')


class Newsmaker(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    email = models.EmailField(blank=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=36, blank=True)
    last_name = models.CharField(max_length=36, blank=True)
    date_birth = models.DateField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse('user-details', args=[str(self.id)])

    def administrator(self):
        self.is_staff = True
        self.save()

    def moderator(self):
        self.is_moderator = True
        self.save()



class Post(models.Model):
    title = models.CharField(max_length=50, default='Without title')
    description = RichTextUploadingField(blank=True, null=True)
    text = RichTextField(blank=True, null=True)
    owner = models.ForeignKey(to='Newsmaker', on_delete=models.CASCADE, related_name='post_owner')
    date_posted = models.DateTimeField(default=timezone.now)

    moderation = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_posted',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-details', args=[str(self.id)])

    def get_owner_url(self):
        return reverse('user-details', args=[str(self.owner.id)])




class Comment(models.Model):
    related_post = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(to='Newsmaker', on_delete=models.CASCADE, related_name='commentator')
    text = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    def get_author_url(self):
        return reverse('user-details', args=[str(self.author.id)])