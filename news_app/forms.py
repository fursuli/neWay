from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title',
                  'description',
                  'text',
                    ]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class UserForm(UserCreationForm):

    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'date_birth',
                  'email',
                  'password1',
                  'password2')
        field_classes = {'username': UsernameField}
