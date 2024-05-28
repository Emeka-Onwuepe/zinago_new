from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
# from django.core.exceptions import PermissionDenied

from users.models import Staff
# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
            user= request.user
            return HttpResponseRedirect(reverse("publication:publisherView",
            kwargs={"userId":user.id,"sectionId":0,"action":"add"}))
    if request.method=="POST":
        form= AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            try:
                publisher = Staff.objects.get(account=user)
            except Staff.DoesNotExist:
                logout(request)
                form=AuthenticationForm()
                return render(request,"users/login.html",{"form":form})
            
            return HttpResponseRedirect(reverse("publication:publisherView",
            kwargs={"userId":user.id,"sectionId":0,"action":"add"}))
    else:
        form=AuthenticationForm()
    return render(request,"users/login.html",{"form":form})

def logoutView(request):
    if request.method=="POST":
        logout(request)
    return HttpResponseRedirect(reverse('users:loginView'))
