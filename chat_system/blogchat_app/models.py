from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, related
from django.contrib.auth import get_user_model
from django.utils.html import TRAILING_PUNCTUATION_CHARS
from datetime import datetime
from django.urls import reverse
# Create your models here.

User = get_user_model()

class NavbarModel(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    navbar_logo = models.CharField(max_length=100,null=True, blank=True)

class CategoryModel(models.Model):
    category = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f"{self.category}"

class PostModel(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    text = models.CharField(max_length=300,null=True,blank=True)
    video = models.FileField(upload_to='videos_uploaded',null=True,blank=True)
    image = models.ImageField(upload_to='images_uploaded',default='images_uploaded/925667.jpg',null=True,blank=True)  
    category1 = models.ForeignKey('CategoryModel',models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now=True)
    room_code = models.IntegerField(null=True,blank=True)
    def get_absolute_url(self):
       return reverse("my_blog_page")  

class LogoModel(models.Model):
    logo_image = models.ImageField(upload_to = 'logo_uploaded',null = True, blank = True)
    logo_url = models.URLField(null = True, blank = True)

class AboutModel(models.Model):
    headimage = models.ImageField(upload_to='aboutimage_uploaded',null=True,blank=True)
    title = models.CharField(max_length=100,null=True, blank=True)
    text = models.CharField(max_length=400,null=True, blank=True)
    ownimage = models.ImageField(upload_to='aboutimage_uploaded',null=True,blank=True)
    name = models.CharField(max_length=40,null=True, blank=True)
    profession = models.CharField(max_length=40,null=True, blank=True)
    small_inf = models.CharField(max_length=100,null=True, blank=True)

class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

class ContactModel2(models.Model):
    adreess = models.CharField(max_length=100,null=True, blank=True)
    adreessurl = models.URLField(max_length=100,null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    short_imf = models.CharField(max_length=100,null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField()
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE,related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self',on_delete=models.CASCADE,related_name='replies',null=True,blank=True)
         
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.user)

    def reply(self):
        return Comment.objects.filter(reply_to=self)

    @property
    def is_reply_to(self):
        if self.reply_to is not None:
            return False
        return True
class ProfileModel(models.Model):
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField()

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)