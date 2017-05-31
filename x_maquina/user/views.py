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
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Bem-vindo à X-Máquina!")
                return redirect('Home')
            except Exception as e:
                print(e)
                traceback.print_exc()
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})
