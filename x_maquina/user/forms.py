# -*- coding: utf-8 -*-
from django import forms
from django.forms import EmailField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário ou e-mail",
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'class': 'login username-field',
                'name': 'username',
                'placeholder': 'E-mail'}))

    password = forms.CharField(
        label="Senha",
        max_length=60,
        widget=forms.PasswordInput(
            attrs={
                'class': 'login password-field',
                'name': 'password',
                'placeholder': "Senha"}))


class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Nome"
        self.fields['first_name'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                "E-mail já cadastrado!", code='email_registered')
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = user.email
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("first_name", "email", "password1", "password2")
