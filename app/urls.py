from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('download/', views.pullData, name='download'),
    path('upload/', views.UploadFile, name='upload_file'),
    path('send/', views.Email, name='email'),
    path('sendEmails/', views.SendEmails, name='send'),
    path('register/', views.Register, name='register'),
    path('test/', views.pushData, name='test'),
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
    path('updateGrad/<int:id>/<int:demonId>/', views.UpdateGraduateStudies, name='updateGrad'),
    path('updateDemon/<int:id>/', views.UpdateDemonstrator, name='updateDemon'),
    path('deleteExtension/<int:id>/<int:demonId>/', views.DeleteExtension, name='deleteExtension'),
    path('deleteFreeze/<int:id>/<int:demonId>/', views.DeleteFreeze, name='deleteFreeze'),
    path('deleteDispatch/<int:id>/<int:demonId>/', views.DeleteDispatch, name='deleteDispatch'),
    path('deleteUnv/<int:id>/<int:demonId>/', views.DeleteUniversityDegree, name='deleteUnv'),
    path('deleteGrad/<int:id>/<int:demonId>/', views.DeleteGraduateStudies, name='deleteGrad'),
    path('deleteDemon/<int:id>/', views.DeleteDemonstrator, name='deleteDemon'),
    path('getAllEmails/', views.GetAllEmails, name='getAllEmails'),
    path('getLateEmails/', views.GetLateEmails, name='getLateEmails'),
    path('getCollegeEmails/', views.GetCollegeEmails, name='getCollegeEmails'),
    path('reportinsert/<int:demonId>/', views.GraduateStudiesDegreeInsert, name='insertGraduate'),
    path('insertExcellence/<int:demonId>/', views.CertificateExcellenceYearInsert, name='insertExcellence'),
    path('durationInsert/<int:dispatchId>/<int:demonId>/', views.DurationChangeInsert, name='durationInsert'),
    path('getAllUsers/', views.GetAllUsers, name='getAllUsers'),
    path('gett/', views.do_something, name='gett'),
    path('test/', views.Test, name='test'),


]