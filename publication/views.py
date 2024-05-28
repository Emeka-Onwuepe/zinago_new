from django.shortcuts import render, reverse
from django.http import  HttpResponseRedirect

from publication.form import ArticleCreationForm,Section_Form
from users.models import Staff,User
from .models import Section, Article
# from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm

from django.forms import  inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from django.core.mail import send_mail

# Create your views here.

@login_required(login_url="users:loginView")
def publisherView(request, userId,sectionId,action):
    user = User.objects.get(pk=userId)
    sections = Section.objects.all()
    # try:
    #     publisher = Staff.objects.get(account=user)
    # except Staff.DoesNotExist:
    #     logout(request)
        # return HttpResponseRedirect(reverse("publication:register"))
    # if not publisher.verified :
            # return render(request, "publication/nonpublisherview.html", {"username":user.full_name})
        
    article_form = ArticleCreationForm()
    if sectionId != 0:   
        section_instance = Section.objects.get(id=sectionId)
    
    if request.method == "POST" and action == "add":
        form = Section_Form(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('publication:publisherView',
            kwargs={"userId":user.id,"sectionId":0,"action":"view"}))
        else:
            return render(request,"publication/publisherview.html",
                  {'article_form':article_form,"form":form,"sectionId":0,"sections":sections,"user": user})  
              
    if action == "edit":
        if request.method == "POST":
            form = Section_Form(data= request.POST,instance=section_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('publication:publisherView',
                        kwargs={"userId":user.id,"sectionId":0,"action":"view"}))
            else:
                return render(request,"publication/publisherview.html",
                  {'article_form':article_form,"form":form,"sectionId":section_instance.id})
        else:
            return render(request,"publication/publisherview.html",
                  {"form":Section_Form(instance=section_instance),
                   "sectionId":section_instance.id,"action":"edit",
                   "user": user, "article_form": article_form,
                   "sections":sections,})
    
    if action == "delete":
        section_instance.delete()
        return HttpResponseRedirect(reverse('publication:publisherView',
            kwargs={"userId":user.id,"sectionId":0,"action":"view"}))
    
    return render(request, "publication/publisherview.html", {"user": user, "article_form": article_form,
                                                                "sections":sections,"form":Section_Form(),
                                                                "sectionId":0,"action":"add"})   
    
    

@login_required(login_url="login:loginView")
def controlView(request,sectionId):
    publisher = Staff.objects.get(account=request.user)
    section = Section.objects.get(id=sectionId)
    article = section.section_article.all()
    return render(request, "publication/controlview.html", {'publisher': publisher, "section":section,
                                                          'article': article, "user": request.user})

