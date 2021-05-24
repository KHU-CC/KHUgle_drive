from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from account.forms import CustomUserForm


def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            major = form.cleaned_data.get('major')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('KHUgle:index')
    else:
        form = CustomUserForm()
    return render(request, 'account/signup.html', {'form': form})