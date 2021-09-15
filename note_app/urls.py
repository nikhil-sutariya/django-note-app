from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('submit-note/', views.noteform, name='noteform'),
    path('edit-note/<int:id>', views.editnote, name='editnote'),
    path('delete-note/<int:id>', views.deletenote, name='deletenote'),
]
