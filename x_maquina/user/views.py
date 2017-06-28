# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
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


@login_required
def user_update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(
            data=request.POST, user=request.user)
        if form.is_valid():
            u = form.save(commit=False)
            success = True
            if not success:
                messages.error(request, "Falha ao atualizar senha!")
            else:
                messages.error(request, "Senha atualizada!")
            u.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/password.html', {
        'form': form})


def user_reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(
            data=request.POST)
        if form.is_valid():
            form.save()
            success = True
            if not success:
                messages.error(request, "Falha ao redefinir senha!")
            else:
                messages.error(
                    request, "Verifique sua caixa de entrada de email!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = PasswordResetForm()
    return render(request, 'user/password_reset.html', {
        'form': form})
