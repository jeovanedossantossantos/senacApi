from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UserCreationForm
from .models import UsersModel


@admin.register(UsersModel)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm