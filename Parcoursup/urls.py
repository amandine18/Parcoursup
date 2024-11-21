from django.urls import path
from Parcoursup.views import *

urlpatterns = [
    path('', offre_list, name='index'),
    path('home/', home, name='home'),
    path('profiletud/', profiletud, name='profiletud'),
    path('candidate/<int:pk>/', candidater, name='create_candidate'),
    path('candidatures/', mes_candidatures, name='candidatures'),
    path('update/<int:pk>/', update_candidature, name='update_candidate'),
    path('delete/<int:pk>/', delete_candidature, name='delete_candidate'),
    path('login/', user_login, name='loginetud'),
    path('register/', register, name='registeretud'),
    path('logout/', CustomLogoutView.as_view(), name='logoutetud'),
]