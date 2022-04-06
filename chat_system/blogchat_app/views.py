from typing import Text
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import request
from django.shortcuts import render,redirect,get_object_or_404
from blogchat_app.models import  PostModel, AboutModel,ContactModel,Comment, Message,Room
from .forms import ProfileForm, RegisterForm,CommentForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import  PostCreateForm
from django.contrib.auth import get_user_model, authenticate, login 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
User = get_user_model

@login_required(login_url = 'login_page')
# def base_view(request):
# 	context = {}
# 	base_queryset = NavbarModel.objects.all()
# 	logo_queryset = LogoModel.objects.all()
# 	post_queryset = PostModel.objects.all()
# 	context['post_queryset'] = post_queryset
# 	context['logo_queryset'] = logo_queryset
# 	context['base_queryset'] = base_queryset
# 	return render(request, 'base.html',context)

def index_view(request):
    post_queryset = PostModel.objects.all()
    p = Paginator(post_queryset, 2)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number) 
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
   
    return render(request, 'index.html',context)


def post_detail_view(request,post_id):
     context = {}
     comment_queryset = Comment.objects.filter(post__id=post_id)
     context['comment_queryset'] = comment_queryset
     detail_queryset = PostModel.objects.filter(id=post_id).first()
     context['detail_queryset'] = detail_queryset
     if request.method == "POST":
        reply_to_obj = None
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = detail_queryset
            comment.reply_to_id = request.POST.get('reply_to_id')
            if comment.reply_to_id:
                reply_qs = Comment.objects.filter(reply_to__id=comment.reply_to_id)
                if reply_qs.exists() and reply_qs.count() == 1 :
                    reply_to_obj = reply_qs.first()
            reply_to = reply_to_obj
            comment.save()
            return redirect('detail_page',post_id=post_id)
     else:
         form = CommentForm()
         context['form']=form
         return render(request,'post_detail.html',context)
    
    
def register_request(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index_page")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index_page")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("index_page")

def about_view(request):
    context = {}
    about_queryset = AboutModel.objects.all()
    context['about_queryset'] = about_queryset
    return render(request,'about.html',context)

def contact_view(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name',None)
        email = request.POST.get('email',None)
        subject = request.POST.get('subject',None)
        message = request.POST.get('message',None)
        ContactModel.objects.create(
            name = name,
            email = email,
            subject = subject,
            message = message
        )
    return render(request,'contact.html',context)


def my_blog_view(request):

    context = {}
    my_blog_queryset = PostModel.objects.filter(username_id=request.user.id)
    context['my_blog_queryset'] = my_blog_queryset

    return render(request,'my_blog.html',context)
def searchbar(request):
    if request.method == 'GET':
        context = {}
        search = request.GET.get('search')
        post = PostModel.objects.filter(Q(title__icontains=search) | Q(text__icontains=search))
        context['post'] = post
        return render(request,'searchbar.html',context)

def archive_view(request): 
    context = {}
    archive_queryset = PostModel.objects.all()
    context['archives'] = archive_queryset
    return render(request,'archive.html',context) 

def post_archive_view():
    return 

def chathome_view(request):
    return render(request, 'chathome.html')
    
def destroy_view(request, id):  
    employee = PostModel.objects.get(id=id)  
    employee.delete()  
    return redirect("/my-blogs")

def room_view(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def check_view(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send_view(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages_views(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def post_create_view(request):
    context = {}
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = request.user
            form.save()
            return redirect('index_page')
        else:
            context['form'] = form
            return render(request, 'post_create.html',context)

    context['form'] = form
    return render(request, 'post_create.html',context)    

class UpdatePostView(UpdateView):
    model = PostModel
    template_name = 'update_post.html'
    exclude = ['date', 'username','video']
    form_class = PostCreateForm