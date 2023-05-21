from django.contrib.auth import forms

from .models import UsersModel


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model =UsersModel


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = UsersModel