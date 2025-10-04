from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from blog.models import Post, AboutUs, Category, PostComments
from django.core.paginator import Paginator
from .forms import Comment_Post, ContactForm, LoginForm, PostForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
# Create your views here.
# posts = [
#         {'id': 1,'title': 'post1', 'content': 'content of the post 1'},
#         {'id': 2,'title': 'post2', 'content': 'content of the post 2'},
#         {'id': 3,'title': 'post3', 'content': 'content of the post 3'},
#         {'id': 4,'title': 'post4', 'content': 'content of the post 4'},
#     ]

def index(request):
    blog_title = "latest posts"

    all_posts = Post.objects.filter(is_published=True)

    #paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  
    return render(request, "blog/index.html", {'blog_title': blog_title, 'page_obj': page_obj})

def detail(request, slug):
    # Permission check
    if request.user and not request.user.has_perm("blog.view_post"):
        messages.error(request, 'You must login to view this post.')
        return redirect('home')
    
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('created_at')
    categories = Category.objects.all()
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.id)

    if post.user != request.user:
    
       if request.user not in post.views.all():
          post.views.add(request.user)

    

    # Handle comment POST
    if request.method == 'POST':
        content = request.POST.get('comment')
        if request.user.is_authenticated:
            PostComments.objects.create(
                post=post,
                name=request.user.username,
                content=content,
                user=request.user,
                email=request.user.email
            )
            messages.success(request, "Comment added successfully!")
            return redirect('detail', slug=slug)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('detail', slug=slug)

    return render(request, "blog/detail.html", {
        'post': post,
        'categories': categories,
        'related_posts': related_posts,
        'comments': comments
    })

def delete_comment(request, id):
    comment = get_object_or_404(PostComments, id=id)
    if request.user == comment.user:
        comment.delete()
    return redirect('detail', slug=comment.post.slug)

def contact_view(request):
    if request.method == 'POST':
       form = ContactForm(request.POST)
       name = request.POST.get('name')
       email = request.POST.get('email')
       message = request.POST.get('message')
       logger = logging.getLogger("TESTING")
       if form.is_valid():
          logger.debug(f"post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}")
          #send email or save in database
          success_message = 'your email has been sent!'
          return render(request, "blog/contact.html", {'form': form, 'success_message':success_message})  

       else:
           logger.debug('form validation failed')

       return render(request, "blog/contact.html", {'form': form, 'name': name, 'email': email, 'meassge': message })   
    return render(request, "blog/contact.html")


def about_view(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content="default content"
    else:
        about_content = AboutUs.objects.first().content
    return render(request, 'blog/about.html', {'about_content': about_content })


def dashboard_view(request):
    blog_title = "My posts"
    all_posts = Post.objects.filter(user = request.user)#.exclude(slug='')
    posts = Post.objects.filter(user=request.user)
    post_comments  = PostComments.objects.filter(user=request.user)
    total_likes = sum(post.likes.count() for post in posts)
    total_comments =  post_comments.count()

    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'blog/dashboard.html', {
         'blog_title' : blog_title,
         'page_obj' : page_obj,
         'total_likes' : total_likes,
         'total_comments' : total_comments,
         })


@login_required
@permission_required('blog.add_post', raise_exception=True)
def new_post_view(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # post.slug = slugify(post.titles)
            post.image_urls = form.cleaned_data.get('image_urls')
            post.save() 
            return redirect('dashboard')
    else:
        form = PostForm()    

    return render(request, 'blog/new_post.html', {
        'categories' : categories,
        'form' : form,
                                                  })

@login_required
def delete_post(request, post_id):
    post = Post.objects.filter(pk=post_id)
    post.delete()
    return redirect('dashboard')
@login_required
def edit_post(request, post_id):

    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', { 'categories' : categories,'post' : post, 'form': form })

@permission_required('blog.can_publish', raise_exception=True)
def publish_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request, "post is published successfully")
    return redirect('dashboard')

# def comment_on_post(request, slug):
#     post  = get_object_or_404(Post, slug=slug)
#     comments = post.comments.all().oder_by('created_at') 

#     if request.method == 'POST':
#        form = Comment_Post(request.Post)
#        if form.is_valid():
#           comment = form.save(commit=False)
#           comment.post = post
#           comment.save()
#           return redirect('detail', slug=slug)
#     else:
#         Comment_Post()
#     context = {
#         'post': post,
#         'comments': comments,
#         'form': form
#     }    
#     return render(request, 'blog/detail.html', {'context' : context})  
   

       

def profile(request):
    return render(request, 'blog/profile.html')

def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('detail', slug=slug)  # adjust 'post_detail' as per your url name

# def view_post(request, slug):
#     post = get_object_or_404(Post, slug=slug)

#     if request.user not in post.views.all():
#         post.views.add(request.user)
#     return  redirect('detail', slug=slug)

# --------------------------------------------------------------authentication-------------------------------------------------------------------------

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            #add user to readers group
            readers_group, ceated = Group.objects.get_or_create(name="Readers") 
            user.groups.add(readers_group)
              
            messages.success(request, "registration successful")
            return redirect('login')
            
    return render(request, 'blog/register.html', {'form': form })

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()            
    return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')




class MyPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html' 