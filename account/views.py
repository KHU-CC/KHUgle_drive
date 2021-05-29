from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from account.forms import CustomUserForm
import bucket.s3_work as s3

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
            s3.create_bucket('khugle-drive-' + username)
            return redirect('KHUgle:index')
    else:
        form = CustomUserForm()
    return render(request, 'account/signup.html', {'form': form})