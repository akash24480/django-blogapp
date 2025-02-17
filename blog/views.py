from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Blog

# Create your views here.

def index(request):
    return render(request, 'index.html')


def user_register(request):
    if(request.method ==  'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check that user is already in the database through email
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email is already registered")
            return redirect('register')
        
        #Now we can create the user manually and save it to the database
        user = User.objects.create_user(username = username, email = email, password = password)
        login(request, user)
        messages.success(request, "You are now logged in")
        return redirect('index')
    
    return render(request, 'register.html')



def user_login(request):
    if(request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
            user = authenticate(username = user.username, password = password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')



# Blog create and update and delete and fetch all for the admin dashboard

@login_required
def blog_list(request):
    blogs = Blog.objects.filter(author = request.user).order_by('-created_at')
    print(blogs, "blogs")
    return render(request, 'dashboard/index.html', {'blogs': blogs})


@login_required
def create_blog(request):
    blogs = Blog.objects.filter(author = request.user).order_by('-created_at')
    if request.method == 'POST':

        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        content = request.POST.get('content')
        image = request.FILES.get('image') if 'image' in request.FILES else None


        # Save blog
        blog = Blog.objects.create(
            author=request.user,
            title=title,
            short_description=short_description,
            content=content,
            image=image
        )

        messages.success(request, "Blog created successfully ✅")
        return redirect('create_blog') # Ensure 'blog_index' is correct

    return render(request, 'dashboard/index.html', {'blogs': blogs})


@login_required
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author != request.user:
        messages.error(request, "You are not the owner of this blog")
        return redirect('create_blog')
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.short_description = request.POST.get('short_description')
        blog.content = request.POST.get('content')

        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        
        blog.save()
        messages.success(request, "Blog updated successfully ✅")
        return redirect('create_blog')
    
    return render(request, 'dashboard/index.html', {'blog': blog})




@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
     # Checking  if the logged-in user is the owner
    if blog.author == request.user:
        blog.delete()
        messages.success(request, "Blog deleted successfully ✅")
    else:
        messages.error(request, "You are not the owner of this blog")
    return redirect('create_blog')