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
            request.session.set_expiry(0)  #user session terminates on browser close
            #reuest.session.set_expiry(600) #user session terminates every 10 min
            auth.login(request, user)
            # messages.success(request, 'You are logged in now')
            return redirect ('choice')
        else:
            messages.error(request, "Неправильные учетные данные, попробуйте еще раз")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
        auth.logout(request)
        # messages.success(request, 'Вы вышли из системы')
        return redirect('login')
