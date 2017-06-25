# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, UserChangeForm
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


@login_required
def user_profile(request):
    if request.method == 'POST':
        profile_form = UserChangeForm(
            data=request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            success = True
            if not success:
                messages.error(request, "Falha ao salvar solicitação!")
            else:
                messages.error(request, "Dados atualizados!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        profile_form = UserChangeForm(instance=request.user)
    return render(request, 'user/profile.html', {
        'form': profile_form})
