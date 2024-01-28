from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('userFeed/', UserFeedView.as_view(), name='userFeed'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('createPost/', CreatePostView.as_view(), name='createPost'),
]
