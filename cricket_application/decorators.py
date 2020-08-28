from django.shortcuts import redirect
from django.contrib.auth.models import User

def unauthenticated_user(view_func):
    def wrapper_func1(request,*args,**kwargs):
        if request.user.is_authenticated:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('cricket_application:login')
    return wrapper_func1