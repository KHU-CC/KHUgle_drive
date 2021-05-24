from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from .models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):

        model = CustomUser
        fields = ('username', 'email', 'major')