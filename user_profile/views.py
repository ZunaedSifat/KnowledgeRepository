from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('feed')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'user_profile/login.html')


@login_required(login_url="/profile/login/")
def logout(request):
    if request.user:
        print("post request detected")
        auth.logout(request)
        messages.success(request, 'You are now logged out')

    return redirect('login')


@login_required(login_url="/profile/login/")
def feed(request):
    return render(request, 'user_profile/feed.html')
