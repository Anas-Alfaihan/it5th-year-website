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
    path('query/', views.QueryDemonstrator, name='query'),
    path('allDemonstrators/', views.getAllDemonstrators, name='allDemonstrators'),
    path('demonstrator/<int:id>/', views.getDemonstrator, name='demonstrator'),
    path('dispatch/<int:demonId>/', views.DispatchInsert, name='dispatch'),
    path('getdispatch/<int:dispatchId>/', views.getDispatch, name='getdispatch'),
    path('extinsert/<int:dispatchId>/<int:demonId>/', views.ExtensionInsert, name='extinsert'),
    path('freinsert/<int:dispatchId>/<int:demonId>/', views.FreezeInsert, name='freinsert'),
    path('reportinsert/<int:dispatchId>/<int:demonId>/', views.ReportInsert, name='reportinsert'),
    path('updateExtension/<int:id>/<int:demonId>/', views.UpdateExtension, name='updateExtension'),
    path('updateFreeze/<int:id>/<int:demonId>/', views.UpdateFreeze, name='updateFreeze'),
    path('updateDispatch/<int:id>/<int:demonId>/', views.UpdateDispatch, name='updateDispatch'),
    path('updateUnv/<int:id>/<int:demonId>/', views.UpdateUniversityDegree, name='updateUnv'),
    path('updateDemon/<int:id>/', views.UpdateDemonstrator, name='updateDemon'),
    path('getAllEmails/', views.GetAllEmails, name='getAllEmails'),
    path('getLateEmails/', views.GetLateEmails, name='getLateEmails'),
    path('getCollegeEmails/', views.GetCollegeEmails, name='getCollegeEmails'),
    path('gett/', views.do_something, name='gett'),


]
