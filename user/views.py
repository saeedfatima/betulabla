from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'coordinator':
                return redirect('coordinator_dashboard')
            elif user.role == 'head':
                return redirect('head_dashboard')
            elif user.role == 'staff':
                return redirect('home')  # Or a staff-specific dashboard
            else:
                messages.error(request, 'Role not authorized.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'users/login.html')
