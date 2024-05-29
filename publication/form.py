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
    
class PublishArticleForm(forms.ModelForm):
    """Form definition for PublishArticleForm."""

    class Meta:
        """Meta definition for PublishArticleFormform."""

        model = Article
        fields = ('publish',)