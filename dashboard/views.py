from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .mixin import LoginRequired
from userprofile.models import UserProfile
from useraction.models import Post, PostApply, PostComment, PostReaction, UserConversation
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# # Create your views here.

class CustomVariables:
    pass

class DashboardView(LoginRequired, View):
    def get(self, request):
        user = request.user
        if user.is_superuser:
            return render(request, 'dashboard/base.html', {'msg' : 'This is admin'})
        else:
            context = {
                'user' : user,
            }
            return render(request, 'dashboard/base.html', context)
        

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
    

class ChangeProfilePicView(View):
    def get(self, request):
        return render(request, 'dashboard/changeProfilePic.html')
    
    def post(self, request):
        user = request.user
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            user.profile_picture = profile_picture
            user.save() 
        return redirect('dashboard')
    
        
class UserFeedView(LoginRequired, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.all()
        applies = PostApply.objects.filter(applied_by = user)
        filtered_applies = [i.post.id for i in applies]
        reacted_posts = PostReaction.objects.filter(reacted_by = user)
        context = {
            'user' : user,
            'posts' : posts,
            'reacted_posts' : reacted_posts,
            'filtered_applies' : filtered_applies
        }
        return render(request, 'dashboard/userFeed.html', context)
     
    def post(self, request):
        user = request.user
        if request.POST['form-num'] == '1':
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id = post_id)
            reaction, created = PostReaction.objects.get_or_create(post = post, reacted_by = user)
            if created:
                reaction.is_liked = True
            else:
                reaction.is_liked = not reaction.is_liked
            reaction.save()
        elif request.POST['form-num'] == '2':
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id = post_id)
            apply = PostApply(post = post, applied_by = user)
            apply.save()
        return redirect('userFeed')
    

class CreatePostView(LoginRequired, View):
    def get(self, request):
        return render(request, 'dashboard/createPost.html')

    def post(self, request):
        added_by = request.user
        description = request.POST['description']
        if 'media' in request.FILES:
            media = request.FILES['media']
            post = Post(added_by = added_by, description = description, media = media)
        else:
            post = Post(added_by = added_by, description = description)
               
        post.save()
        return redirect('userFeed')


class EditPostView(LoginRequired, View):
    def get(self, request, **kwargs):
        post = Post.objects.get(id = kwargs['post_id'])
        if request.user == post.added_by:
            context = {
                'post' : post
            }
            return render(request, 'dashboard/editpost.html', context)
        else:
            return redirect('userFeed')
    
    def post(self, request, **kwargs):
        post = Post.objects.get(id = kwargs['post_id'])
        description = request.POST['description']
        if 'media' in request.FILES:
            media = request.FILES['media']
            post.description = description
            post.media = media
        else:
            post.description = description
        post.save()
        return redirect('userFeed')


class DeletePostView(View):
    def get(self, request, **kwargs):
        post = Post.objects.get(id = kwargs['post_id'])
        if request.user == post.added_by:
            post.delete()
        return redirect('userFeed')

    
    # def get(self, request):
    #     user = request.user
    #     applicants = [applicant for applicant in PostApply.objects.all() if applicant.applied_by != user]
    #     post_and_applicants = [(application.post.added_by, application.applied_by) for application in PostApply.objects.all()]
    #     unpacked_users = [item for tuple in post_and_applicants for item in tuple]
    #     if user not in unpacked_users:
    #         data = False
    #     elif user in unpacked_users:
    #         data = True
    #     filtered_applicants = []
    #     unique_post_ids = set()
    #     for applicant in applicants:
    #         post_id = applicant.post.id
    #         if post_id not in unique_post_ids:
    #             unique_post_ids.add(post_id)
    #             filtered_applicants.append(applicant)
    #     context = {
    #         'filtered_applicants' : filtered_applicants,    
    #         'data' : data
    #     }
    #     return render(request, 'dashboard/applicants.html', context)

class ApplicantsView(LoginRequired, View):
    def get(self, request):
        user = request.user
        applicants = PostApply.objects.filter(post__added_by_id = user.id, is_approved = False)
        context = {
            'applicants' : applicants
        }
        return render(request, 'dashboard/applicants.html', context)

    
    def post(self, request):
        user = request.user
        applicant_id = request.POST.get('applicant_id')
        applicant = PostApply.objects.get(id = applicant_id)
        post = Post.objects.get(id = applicant.post.id)
        applicant.is_approved = True
        UserConversation.objects.create(post = post, message_by = user, applicant = applicant) 
        applicant.save()
        return redirect('applicants')
    

    # def get(self, request):
        # user = request.user
        # chats = [conversation for conversation in UserConversation.objects.all() if conversation.applicant != user]
        # posts_and_applicants = [(conversation.post.added_by, conversation.applicant.applied_by) for conversation in UserConversation.objects.all()]
        # unpacked_users = set([item for tuple in posts_and_applicants for item in tuple])
        # if user not in unpacked_users:
        #     data = False
        # elif user in unpacked_users:
        #     data = True
        # filtered_chats = []
        # unique_post_ids = set()
        # for conversation in chats:
        #     post_id = conversation.post.id
        #     if post_id not in unique_post_ids:
        #         unique_post_ids.add(post_id)
        #         filtered_chats.append(conversation)
        # context = {
        #     'filtered_chats' : filtered_chats,
        #     'data' : data
        # }
class UserConversationView(LoginRequired, View):
    def get(self, request):
        user = request.user
        applicants = PostApply.objects.filter(Q(post__added_by_id = user.id) | Q(applied_by = user), is_approved = True)
        context = {
            'applicants' : applicants
        }
        print(applicants)
        return render(request, 'dashboard/messages.html', context)
    

class UserChatView(LoginRequired, View):
    def get(self, request, **kwargs):
        user = request.user
        post = Post.objects.get(id = kwargs['post_id'])
        applicant = PostApply.objects.get(id = kwargs['applicant_id'])
        chats = UserConversation.objects.filter(post = post, applicant = applicant)
        context = {
            'chats' : chats,
            'message_by' : chats[0].message_by.username,
            'applicant' : chats[0].applicant.applied_by,
            'user' : user,

        }
        print(context['message_by'], context['applicant'], user)
        return render(request, 'dashboard/userMessage.html', context)

    def post(self, request, **kwargs):
        post = Post.objects.get(id = kwargs['post_id'])
        applicant = PostApply.objects.get(id = kwargs['applicant_id'])
        message = request.POST['message']
        chat = UserConversation(post = post, message_by = request.user , applicant = applicant, message = message,)
        chat.save()
        return redirect('userChat', post_id=post.id, applicant_id=applicant.id)
        


    
