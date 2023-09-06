from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('members/', views.members, name='members'),
    path('about/', views.about, name='about'),
    path('members/details/<int:id>', views.details, name='details'),
    path('members/portfolio/', views.portfolio, name='portfolio'),
    path('', views.home, name='home'),
    path('members/rate/', views.rate, name='rate'),
    path('members/rate/<int:id>', views.edit, name='edit'),
    path('members/delete/<int:id>', views.delete, name='delete'),
    path('test', views.test, name='test'),
    path('my_api', views.api, name='api'),
    path('analysis_main', views.analysis, name='analysis'),
    path('analysis_main/project1', views.project1, name='analysis1'),
    path('analysis_main/project2', views.project2, name='analysis2'),
    path('analysis_main/project3', views.project3, name='analysis3'),
    path('analysis_main/project4', views.project4, name='analysis4'),
]