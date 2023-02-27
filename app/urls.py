from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.Register, name='register'),
    path('test/<int:id>', views.Test, name='test'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('insert/', views.DemonstratorInsert2, name='insert'),
    path('update/<int:id>', views.UpdateDemonstrator, name='update'),
    path('query/', views.QueryDemonstrator, name='query'),
    path('allDemonstrators/', views.getAllDemonstrators, name='allDemonstrators'),
    path('demonstrator/<int:id>/', views.getDemonstrator, name='demonstrator'),
    path('dispatch/<int:demonId>/', views.DispatchInsert, name='dispatch'),
    path('getdispatch/<int:dispatchId>/', views.getDispatch, name='getdispatch'),
    path('extinsert/<int:dispatchId>', views.ExtensionInsert, name='extinsert')


]
