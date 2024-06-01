from django.shortcuts import render,reverse
from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from publication.models import Article
from users.models import Staff
from .models import Application
# Create your views here.
@login_required(login_url="users:loginView")
def applicationView(request, article_id):
    post = None
    try: 
        post = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return HttpResponseRedirect(reverse("publication:publisherView",
        kwargs={"username":request.user.username,"sectionId":0,"action":"add"}))
    applications = post.post_applications.filter(selected=False)
    selected = post.post_applications.filter(selected=True)
    total = len(applications) + len(selected)
    publisher = Staff.objects.get(account=request.user)
    return render(request, "applications/applications.html", {'post':post,'publisher':publisher,
                                                            "applications":applications,"total":total,
                                                            'selected':selected
                                                            })
    
@login_required(login_url="users:loginView")
def process_application(request,app_id,action):
    application = None
    
    try: 
            application = Application.objects.get(id=app_id)
    except Application.DoesNotExist:
            return HttpResponseRedirect(reverse("publication:publisherView",
            kwargs={"username":request.user.username,"sectionId":0,"action":"add"}))
    
    if action == "select":
        application.selected = True
        application.save()
    
    if action == "unselect":
        application.selected = False
        application.save()
        
    if action == "employed":
        application.employed = True
        application.save() 
        
    return HttpResponseRedirect(reverse('applications:applications',
                                                kwargs={"article_id":application.job_id}))

