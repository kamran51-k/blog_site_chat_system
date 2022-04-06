from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Comment, PostModel, ProfileModel
from blogchat_app import models
from django.contrib.auth import get_user_model

# Create your forms here.

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'cols':15}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ('first_name','last_name','email')

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        exclude = ['date', 'username','video']
