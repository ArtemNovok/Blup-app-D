from django.urls import path
from . import views


app_name = "feed"

urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path("new/", views.CreatePost.as_view(), name='new'),
    path("followed/", views.FollowedView.as_view(), name='followed')
]
