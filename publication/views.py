from django.shortcuts import render, reverse
from django.http import  HttpResponseRedirect

from publication.form import ArticleCreationForm, PublishArticleForm,Section_Form
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
    
    if request.method == "POST" and action == "add_post":
        form = ArticleCreationForm(data= request.POST,files=request.FILES)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse('publication:controlView',
            kwargs={"sectionId":post.section.id}))
        else:
            return render(request,"publication/publisherview.html",
                  {'article_form':form,"form":form,"sectionId":0,"sections":sections,"user": user}) 
              
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


@login_required(login_url="user:loginView")
def editview(request,article_id,action):
    article = Article.objects.get(pk=article_id)
    article_form = ArticleCreationForm(instance=article)
    if request.method == "POST" and action == 'edit':
        form = ArticleCreationForm(data= request.POST,files=request.FILES,instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('publication:controlView',
            kwargs={"sectionId":article.section.id}))
             
    return render(request, "publication/editview.html", {'article_id':article.id,
                                                         'article_form':article_form})

@login_required(login_url="login:loginView")
def articlePublisherView(request, article_id):
    article = Article.objects.get(pk=article_id)
    # article_sections = Sections.objects.filter(article=article)
    form = PublishArticleForm(instance=article)
    nullvalue = "<p>null</p>" or "null"
    return render(request, "publication/articlePublisherView.html",
                  {"article": article, "form": form, "nullvalue": nullvalue})
    
    
@login_required(login_url="users:loginView")
def articleWithdrawView(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == "POST":
        article.publish = False
        slug = article.title_slug
        transformedSlug = f"{slug}-transformedslugdjango"
        article.title_slug = transformedSlug
        article.save(),
        return HttpResponseRedirect(reverse('publication:controlView',
                                            kwargs={"sectionId": article.section.id}))
        

@login_required(login_url="users:loginView")
def publishView(request, article_id, article_slug):
    user = request.user
    article = Article.objects.get(pk=article_id)
    form = PublishArticleForm(request.POST, instance=article)
    if form.is_valid():
        removeaddedslug = article.title_slug
        article.title_slug = re.sub(
            r"(-transformedslugdjango)", "", removeaddedslug)
        article.save()
        form.save()
        messages.add_message(request, messages.INFO,
                                 "Article published Successfully")
        return render(request, "publication/articlePublisherView.html",
                          {"article": article, "user": user})
    else:
        return render(request, "publication/articlePublisherView.html",
                          {"article": article, "user": user, "message": "An Error occured"})

@login_required(login_url="users:loginView")
def articleDeleteView(request, article_id):
    article = Article.objects.get(pk=article_id)
    user = request.user
    if request.method == "POST":
        article.delete()
        return HttpResponseRedirect(reverse('publication:controlView', kwargs={"sectionId": article.section.id}))
    

@login_required(login_url="users:loginView")
def close_application(request, article_id, action):
    article = Article.objects.get(pk=article_id)
    user = request.user
    if request.method == "POST" and action == "close":
        article.still_open = False
        article.save()
    else:
        article.still_open = True
        article.save()
    return HttpResponseRedirect(reverse('publication:controlView', kwargs={"sectionId": article.section.id}))