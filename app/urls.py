from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('insert/', views.DemonstratorInsert2, name='insert'),
    path('update/<int:id>', views.UpdateDemonstrator, name='update'),
    path('query/', views.QueryDemonstrator, name='query'),
    path('allDemonstrators/', views.getAllDemonstrators, name='allDemonstrators'),

]
