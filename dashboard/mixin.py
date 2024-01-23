from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse

class LoginRequired(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')