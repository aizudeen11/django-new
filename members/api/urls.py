from django.urls import path
from. import views

urlpatterns = [
    path('', views.getRoutes),
    path('members/', views.getMembers),
    path('comment/', views.getComment)
]