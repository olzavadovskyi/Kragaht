from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # CKEditor

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'category']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        }
