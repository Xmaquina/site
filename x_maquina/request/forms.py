# -*- coding: utf-8 -*-
from django.forms import ModelForm, ClearableFileInput
from django import forms

from request.models import Request


class RequestForm(ModelForm):

    class Meta:
        model = Request
        fields = ['cnc_option', 'cad_file']
        widgets = {
            'cad_file': forms.FileInput(
                attrs={
                    'style': 'margin:10px; width:90%',
                    'class': 'btn btn-default',
                    'accept': '.stl, .STL, .dxf, .DXF'}),
        }
