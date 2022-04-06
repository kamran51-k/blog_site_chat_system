from django.contrib import admin
from django.contrib import admin
from .models import Room, Message
from blogchat_app.models import AboutModel, CategoryModel, Comment, ContactModel, LogoModel, NavbarModel, PostModel, ContactModel2, ProfileModel

# Register your models here.
admin.site.register(NavbarModel)
admin.site.register(PostModel)
admin.site.register(LogoModel)
admin.site.register(AboutModel)
admin.site.register(ContactModel2)
admin.site.register(ContactModel)
admin.site.register(Comment)
admin.site.register(CategoryModel)
admin.site.register(ProfileModel)
admin.site.register(Room)
admin.site.register(Message)