# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from .forms import UserCreationForm
import traceback


def user_logout(request):
    logout(request)
    return redirect('user:Login')


def registrate(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        success = False
        if form.is_valid():
            try:
                user = form.save()
                login(user)
                success = True
            except Exception as e:
                success = False
                print(e)
                traceback.print_exc()
        if not success:
            messages.error(request, "Falha de registro!")
        else:
            messages.success(request, _("Entry saved!"))
            return redirect('Home')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})
