from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('userFeed/', UserFeedView.as_view(), name='userFeed'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('changeProfilePic/', ChangeProfilePicView.as_view(), name='changeProfilePic'),
    path('createPost/', CreatePostView.as_view(), name='createPost'),
    path('applicants/', ApplicantsView.as_view(), name='applicants'),
    path('message/', UserConversationView.as_view(), name='message'),
    path('userChat/<int:post_id>/<int:applicant_id>', UserChatView.as_view(), name='userChat' ),
    path('editpost/<int:post_id>', EditPostView.as_view(), name='editpost'),
    path('deletepost/<int:post_id>', DeletePostView.as_view(), name='deletepost')
]
