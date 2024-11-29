from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # built-in form provided by Django for user signup
from django.contrib.auth import authenticate, login,logout
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('home')  # Redirect to the home page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or wherever
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)  # Logs the user out
    return redirect('home')  # Redirect to home or wherever you want

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your blog post has been created successfully!')
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

def view_post(request, id):
    # Print the id to check if it's passed correctly
    print(f"ID received in view_post: {id}")
    
    # Fetch the post using the ID
    post = get_object_or_404(BlogPost, id=id)
    
    return render(request, 'view_post.html', {'post': post})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)  # Retrieve the post to be updated

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)  # Bind the form with existing post data
        if form.is_valid():
            form.save()  # Save the updated post
            return redirect('home')  # Redirect to the home page or the post detail page
    else:
        form = BlogPostForm(instance=post)  # Display the form with the current post data

    return render(request, 'edit_blog_post.html', {'form': form})


@login_required
# def delete_blog_post(request, post_id):
#     post = get_object_or_404(BlogPost, id=post_id, author=request.user)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('home')  # Redirect to the home page after deletion
#     return render(request, 'delete_blog_post.html', {'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)  # Retrieve the post to delete

    if request.method == 'POST':  # If the form is submitted
        post.delete()  # Delete the post from the database
        return redirect('home')  # Redirect to the home page or post list after deletion

    return render(request, 'delete_blog_post.html', {'post': post})



