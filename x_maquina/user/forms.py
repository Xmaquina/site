from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário ou e-mail",
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'class': 'login username-field',
                'name': 'username',
                'placeholder': 'Usuário ou e-mail'}))

    password = forms.CharField(
        label="Senha",
        max_length=60,
        widget=forms.PasswordInput(
            attrs={
                'class': 'login password-field',
                'name': 'password',
                'placeholder': "Senha"}))
