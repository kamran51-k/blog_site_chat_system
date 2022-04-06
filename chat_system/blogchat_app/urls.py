from os import name
from django.urls import path
from .views import about_view,index_view, contact_view, my_blog_view,register_request,login_request,destroy_view,logout_request,post_detail_view,UpdatePostView, searchbar,archive_view,post_archive_view,room_view,chathome_view,post_create_view,check_view,getMessages_views,send_view

urlpatterns = [
    path('',index_view,name='index_page'),
    path('post-detail/<int:post_id>/',post_detail_view,name='detail_page'),
    path("register", register_request, name="register_page"),
    path("login", login_request, name="login_page"),
    path("logout", logout_request, name="logout_page"),
    path('about',about_view,name='about_page'),
    path('contact-us',contact_view,name='contact_page'),
    path('my-blogs',my_blog_view,name='my_blog_page'),
    path('searchbar',searchbar,name='searchbar'),
    path('archive',archive_view,name='archive_page'),
    path('archive', post_archive_view, name='post_archive_page'),
    path("post-create/", post_create_view, name = 'post_create_page'),
    path('chat-home', chathome_view, name='home'),
    path('<str:room>/', room_view, name='room'),
    path('checkview', check_view, name='checkview'),
    path('send', send_view, name='send'),
    path('getMessages/<str:room>/', getMessages_views, name='getMessages'),  
    path('delete/<int:id>', destroy_view, name='dest_page'),  
    path('article/edit/<int:pk>', 
      UpdatePostView.as_view(), name="update_post"),
     
]

