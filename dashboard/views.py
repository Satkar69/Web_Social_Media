from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .mixin import LoginRequired
from userprofile.models import UserProfile
from useraction.models import Post, PostApply, PostComment, PostReaction
from django.core.exceptions import ObjectDoesNotExist

from .forms import *
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
    
        
class UserFeedView(LoginRequired, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.all()
        reactions = PostReaction.objects.all()
        new_reactions = [reaction.post.id for reaction in reactions if reaction.reacted_by == user ]
        reacted_posts = PostReaction.objects.filter(reacted_by = user)
        print(new_reactions)
        context = {
            'user' : user,
            'posts' : posts,
            'reactions' : reactions,
            'reacted_posts' : reacted_posts,
            'new_reactions' : new_reactions
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


    
class ApplicantsView(View):
    def get(self, request):
        user = request.user
        applicants = [applicant for applicant in PostApply.objects.all() if applicant.applied_by != user]
        filtered_applicants = []
        unique_post_ids = set()
        for applicant in applicants:
            post_id = applicant.post.id
            if post_id not in unique_post_ids:
                unique_post_ids.add(post_id)
                filtered_applicants.append(applicant)
        context = {
            'filtered_applicants' : filtered_applicants
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

class UserConversationView(View):
    def get(self, request):
        user = request.user
        chats = [conversation for conversation in UserConversation.objects.all() if conversation.applicant != user]
        filtered_chats = []
        unique_post_ids = set()
        for conversation in chats:
            post_id = conversation.post.id
            if post_id not in unique_post_ids:
                unique_post_ids.add(post_id)
                filtered_chats.append(conversation)
        context = {
            'filtered_chats' : filtered_chats
        }
        return render(request, 'dashboard/messages.html', context)

class UserChatView(View):
    def get(self, request, **kwargs):
        user = request.user
        post = Post.objects.get(id = kwargs['post_id'])
        applicant = PostApply.objects.get(id = kwargs['applicant_id'])
        chats = UserConversation.objects.filter(post = post, applicant = applicant)
        context = {
            'chats' : chats,
            'applicant_name' : applicant.applied_by
        }
        return render(request, 'dashboard/userMessage.html', context)

    def post(self, request, **kwargs):
        post = Post.objects.get(id = kwargs['post_id'])
        applicant = PostApply.objects.get(id = kwargs['applicant_id'])
        message = request.POST['message']
        chat = UserConversation(post = post, message_by = request.user , applicant = applicant, message = message,)
        chat.save()
        return redirect('userChat/{}/{}'.format(post.id, applicant.id))
        # issue = Issue.objects.get(id=kwargs['id'])
        # message_by = UserProfile.objects.get(username=request.user)
        # message = request.POST.get('message')
        # file = request.FILES.get('file')
        # issue_status_form = IssueStatusForm(instance=issue, data=request.POST)
        # if request.POST['form_num'] == '1':
        #     if issue_status_form.is_valid():
        #         issue_status_form.save()
        # elif request.POST['form_num'] == '2':
        #     if message == "":
        #         issue_conversation = IssueConversation.objects.create(
        #             issue=issue,
        #             message_by=message_by,
        #             file = file,
        #             created_at=timezone.now(),
        #             updated_at=timezone.now()
        #         )
        #     else:
        #         issue_conversation = IssueConversation.objects.create(
        #             issue=issue,
        #             message_by=message_by,
        #             message=message,
        #             file = file,
        #             created_at=timezone.now(),
        #             updated_at=timezone.now()
        #         )
        #         issue_conversation.save()
        


    
