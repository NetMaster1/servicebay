from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate

# Create your views here
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'You are logged in now')
            return redirect ('choice')
        else:
            # messages.error(request, "Invalid credentials. Please, try again")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')
