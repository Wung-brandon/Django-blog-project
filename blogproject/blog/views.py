from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm, UserForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q


# Create your views here.
@login_required(login_url='login')
def listPosts(request, query=None):
    user = request.user
    # Get or create the user profile
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    # if created:
    #     messages.success(request, "User profile was not found, so a new one has been created.")
    
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__username__icontains=q)
        ).annotate(comment_count=Count('comments')).order_by('-created')
        
        if not posts.exists():
            messages.info(request, "Nothing found")
            posts = Post.objects.all().annotate(comment_count=Count('comments'))
    else:
        posts = Post.objects.all().annotate(comment_count=Count('comments')).order_by('-created')
        query = ""
    
    context = {
        'posts': posts,
        'user': user,
        'user_profile': user_profile,
        'q': query
    }
    return render(request, 'index.html', context)    

def detail(request, pk):
    post = get_object_or_404(Post.objects.annotate(comment_count=Count('comments')), id=pk)
    comments = Comment.objects.filter(post=post).select_related('author')
    user_profile, created = UserProfile.objects.get_or_create(user=post.author)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('comment-post', pk=pk)
    else:
        form = CommentForm()
    
    context = {
        'post':post,
        'user_profile':user_profile,
        'comments':comments
        }
    
    return render(request, 'detail.html', context)

login_required(login_url='login')
def createPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to database yet
            if request.user.is_authenticated:   
                post.author = request.user       # Set the author to the current user
                post.save()  
                # form.save()
                messages.success(request, "Post Created Successfully")
                return redirect('home')
    else:
        form = PostForm()

    context = {
        'form': form
    }
    
    return render(request, 'create_form.html', context)

def registerUser(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        profile_picture = request.FILES.get('profile_picture')
        if password == confirm_password:
            user_exists = User.objects.filter(username=username).exists()
            email_exists = User.objects.filter(email=email).exists()
            if user_exists:
                messages.info(request, 'User with username already exists')
                return redirect('signup')
            elif email_exists:
                messages.info(request, 'User with email already exists')
                return redirect('signup')
            else:
                
                user = User.objects.create_user(username=username, email=email, password=password)
                user_profile = UserProfile.objects.create(user=user, profile_picture=profile_picture)
                user_profile.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.info(request, 'Password Mismatch')
          
    return render(request, 'signup.html')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # Set session variable to indicate that the welcome message has been shown
            request.session['welcome_message_shown'] = True
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login_form.html')

def logoutUser(request):
    auth.logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('login')
    
 


def forgot_password(request):
    pass

    return render(request, 'forgot_password.html')
login_required(login_url='login')
def editPost(request, pk):
    post = Post.objects.get(id=pk)
    # form = PostForm(instance=posts)
    if request.user != post.author:
        messages.warning(request, "You are not allowed to edit this post")
        # return HttpResponse("You are not allowed to edit this post")
        
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to database yet
            post.author = request.user       # Set the author to the current user
            post.save()  
            messages.success(request, "Post Updated Successfully")
            # form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post':post
    }    
    return render(request, 'edit-form.html', context)

login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    # Check if the current user is the author of the post
    if request.user != post.author:
        messages.warning(request, "You are not allowed to delete this post")
        # Redirect the user to the home page or any other appropriate page
        return redirect('home')
    else:
        if request.method == 'POST' and 'confirm_delete' in request.POST:
            
            post.delete()
            messages.success(request, "Post deleted successfully")
            return redirect('home')
    context = {
        'object':post,
        'object_type': 'post'
    }
    return render(request, 'delete.html', context)
        
@login_required(login_url='login')
def commentPage(request, pk):
    # Retrieve the post and annotate it with the comment count
    post = get_object_or_404(Post.objects.annotate(comment_count=Count('comments')), id=pk)
    comments = Comment.objects.filter(post=post).select_related('author')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('comment-post', pk=pk)
    else:
        form = CommentForm()

    # Create a dictionary to map comment authors to their profiles
    comment_profiles = {comment.author: UserProfile.objects.get(user=comment.author) for comment in comments}
    print(f"comment profiles: {comment_profiles}")
    # user_profile_m, created = UserProfile.objects.get_or_create(user=post.author)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_profiles': comment_profiles,  # Changed key to comment_profiles
        'form': form,
    } 
    return render(request, 'comments.html', context)
    
login_required(login_url='login')
def editComment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.user != comment.author:
        messages.warning(request, "You are not allowed to edit this comment")
        
    if request.method == "POST":
        content = request.POST["content"]
        if content:
            comment.content = content
            comment.save()
            messages.success(request, "Comment updated successfully.")
        else:
            messages.error(request, "Content cannot be empty.")
        
        return redirect('detail', pk=comment.post.id)

    context = {
        'comment':comment
    }    
    
    return render(request, 'edit-comment.html', context)
  
login_required(login_url='login')  
def deleteComment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user != comment.author:
        messages.warning(request, "You are not allowed to delete this Comment")
        # Redirect the user to the home page or any other appropriate page
        return redirect('home')
    else:
        if request.method == 'POST' and "confirm_delete" in request.POST:
            comment.delete()
            messages.success(request, "Comment deleted successfully")
            return redirect('comment-post', pk=comment.post.id)
       
    context = {
        'object': comment,
        'object_type': 'comment'
        }
    return render(request, 'delete.html', context)
    

login_required(login_url='login')
def userProfile(request, pk):
    user = get_object_or_404(User, id=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    context = {
        'user':user,
        'user_profile':user_profile
    }
    
    return render(request, 'user-profile.html', context)


def editProfile(request, pk):
    user = get_object_or_404(User, id=pk)
    user_profile = user.userprofile  # Assuming UserProfile is related to the User model
    form1 = UserProfileForm(instance=user_profile)
    form2 = UserForm(instance=user)
    
    if request.method == 'POST':
        form1 = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        form2 = UserForm(request.POST, instance=user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect('profile', pk=user.id)
        else:
            print(form1.errors, form2.errors)
            messages.error(request, "Profile Did Not Update.")         
            
    context = {
        'form1': form1,
        'form2': form2
    }
    
    return render(request, "edit-profile.html", context)