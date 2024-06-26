from django.urls import path
from . import views

app_name = "publication"

urlpatterns = [
    # path('', views.register, name="register"),
    # path('editProfile', views.editProfile, name="editProfile"),
    # path('editProfilePro', views.editProfilePro, name="editProfilePro"),
    # path('<str:username>/articlecreate',
    #      views.ArticleCreateView, name="articleCreateView"),
    # path('<int:userId>/articlecreation',
        #  views.ArticleCreationView, name="articleCreationView"),
    path('<int:article_id>',
         views.articlePublisherView, name="articlePublisherView"),
    path('publish/<int:article_id>/<slug:article_slug>',
         views.publishView, name="publishView"),
    path('controlview/<int:sectionId>', views.controlView, name="controlView"),
    path('delete/<int:article_id>',
         views.articleDeleteView, name="articleDeleteView"),
    path('withdraw/<int:article_id>', views.articleWithdrawView,
         name="articleWithdrawView"),
    path('close/<int:article_id>/<str:action>', views.close_application,
         name="close"),
    # path('<str:username>/<int:article_id>/editview',
    #      views.editView, name="editView"),
    path('<int:article_id>/<str:action>/editview',
         views.editview, name="editview"),
    path('dashbord/<int:userId>/<int:sectionId>/<str:action>',
         views.publisherView, name="publisherView"),
]
