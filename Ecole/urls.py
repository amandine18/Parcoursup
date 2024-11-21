from django.urls import path
from Ecole.views import *

urlpatterns = [
    path('', offre_list, name='home'),
    # path('indexet/', index_etud, name='indexet'),
    path('profilecole/', profilecole, name='profilecole'),
    path('update_statut/<int:candidate_id>/', update_statut, name='updatestatut'),
    path('create/', create_offre, name='create_offre'),
    path('offres/', mes_offres, name='offres'),
    path('update/<int:pk>/', update_offre, name='update_offre'),
    path('delete/<int:pk>/', delete_offre, name='delete_offre'),
    path('login/', user_login, name='loginecole'),
    path('register/', register, name='registerecole'),
    path('logout/', CustomLogoutView1.as_view(), name='logoutecole'),
]