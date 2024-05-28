from django import forms
from .models import  Article, Section

class ArticleCreationForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ("pub_date","mod_date",
                   'publisher','view_count',
                   'publish','still_open')

class Section_Form(forms.ModelForm):
    class Meta:
        model = Section
        fields = "__all__"
    