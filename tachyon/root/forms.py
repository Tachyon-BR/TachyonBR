from django import forms
from ckeditor.fields import RichTextFormField
from .models import *
from django.forms import ModelForm


class TextMDForm(ModelForm):
    texto = RichTextFormField()
    class Meta:
        model = TextMD
        fields = ['texto']

