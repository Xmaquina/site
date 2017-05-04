from django.forms import ModelForm, ClearableFileInput
from django import forms

from request.models import Request


class RequestForm(ModelForm):

    class Meta:
        model = Request
        fields = ['cad_file']
        widgets = {
            'cad_file': forms.ClearableFileInput(
                attrs={'style':'margin:10px; width:90%','class':'btn btn-default','accept': '.stl, .STL'}),
        }
