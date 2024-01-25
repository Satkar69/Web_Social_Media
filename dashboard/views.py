from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .mixin import LoginRequired
from userprofile.models import UserProfile
from useraction.models import Post, PostBid, PostComment, PostReaction
from .forms import *
# # Create your views here.


class DashboardView(LoginRequired, View):
    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'dashboard/base.html', {'msg' : 'This is admin'})
        else:
            return redirect('userFeed')
        

class RegisterView(View):
    def get(self, request):
        return render(request, 'dashboard/register.html')
    
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = UserProfile.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email)
        user.set_password(password)
        user.save()
        return redirect('login')
    

class LoginView(View):
    def get(self, request):
        return render(request, 'dashboard/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(self.request, user)
            return redirect('dashboard')
        else:
            return render(request, 'dashboard/login.html', {'error' : 'incorrect credentials'})
        
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
        
class UserFeedView(LoginRequired, View):
    def get(self, request):
        posts = Post.objects.all()
        reactons = PostReaction.objects.all()
        context = {
            'posts' : posts,
            'reactions' : reactons
        }
        return render(request, 'dashboard/userFeed.html', context)
    
    def post(self, request):
        pass
    

class CreatePostView(LoginRequired, View):
    def get(self, request):
        return render(request, 'dashboard/createPost.html')

    def post(self, request):
        added_by = request.user
        description = request.POST['description']
        media = request.FILES['media']
        post = Post(added_by = added_by, description = description, media = media)
        post.save()
        return redirect('userFeed')





    
