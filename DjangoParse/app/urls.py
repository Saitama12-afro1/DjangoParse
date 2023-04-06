from django.urls import path
from . import views

urlpatterns = [
    # path('grr/', views.test , name='tttt'),
    path('', views.MyView.as_view(), name="main")
]