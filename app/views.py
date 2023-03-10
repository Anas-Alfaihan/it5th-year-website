import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.utils import ErrorDict
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.apps import apps
from django.db.models import Q
from json import dumps
from .models import *
from .forms import *
from . import forms


@login_required(login_url='app:login')
def Register(request):

    if request.method == 'POST':
        if request.user.is_superuser:
            user = User.objects.create_user(
                username=request.POST['username'],
                first_name=request.POST['firstName'],
                last_name=request.POST['lastName'],
                password=request.POST['password'],
                email=request.POST['email']
            )
            for perm in request.POST.getlist('permissions'):
                permission, created= Permissions.objects.get_or_create(permissionsCollege=perm)
                user.permissions.add(permission.id)
            LastPull.objects.create(userId= user)
            messages.add_message(request, messages.SUCCESS,"أهلاً و سهلاً")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تسجيل موظفين")
            return redirect('app:home')

    if request.user.is_superuser:
        permissions= serializers.serialize('json', Permissions.objects.all(),fields=('permissionsCollege'))
        
        return render(request, 'registration/register.html', {'colleges': permissions })
    else:
        return render(request, 'registration/result.html', {'result': 'denied'})


def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,"أهلاً و سهلاً")
            return redirect('app:home')
        else:
            return render(request, 'registration/result.html', {'result': 'no such a user'})

    return render(request, 'registration/login.html')


def Logout(request):
    logout(request)
    messages.add_message(request, messages.ERROR,"تم تسجيل الخروج")
    return redirect('app:home')


def generalInsert(request, mainField, baseDic, model, addModel, savePoint):
    id = None
    for i in range(len(request.POST.getlist(mainField))):
        dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
        dic.update(baseDic)
        for field in model._meta.local_fields:
            if field.name in request.POST:
                dic[field.name] = request.POST.getlist(field.name)[i]
        form = addModel(dic)
        if form.is_valid():
            id = form.save()
        else:
            transaction.savepoint_rollback(savePoint)
            return form.errors
    return id


def DemonstratorInsert2(request):
    if request.method == 'POST':
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if request.POST['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                demonId = generalInsert(request, 'name', {}, Demonstrator, AddDemonstrator, savePoint)
                if type(demonId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:home')

                id = generalInsert(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:home')

                id = generalInsert(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:home')

                id = generalInsert(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:home')

                id = generalInsert(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم تسجيل المعيد")
            return redirect('app:home')
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')

    else:
        return render(request, 'home/insert.html')


def AdjectiveChangeInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير الصفة")
                    return redirect('app:home')

                demonstrator = Demonstrator.objects.get(pk=demonId)
                demonstrator.currentAdjective = request.POST['adjectiveChangeAdjective']
                Demonstrator.full_clean(self=demonstrator)
                Demonstrator.save()

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير الصفة")
            return redirect('app:home')
        else: 
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')

    else:
        return render(request, 'registration/dispathInsert.html')


def DispatchInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():

                savePoint = transaction.savepoint()

                dispatchId = generalInsert(request, 'dispatchDecisionNumber', {'studentId': demonId}, Dispatch, AddDispatch, savePoint)
                if type(dispatchId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة الإيفاد")
                    return redirect('app:home')

                id = generalInsert(request, 'regularizationDecisionNumber', {'regularizationDecisionId': dispatchId}, Regularization, AddRegularization, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة الإيفاد")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة الإيفاد")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')

    else:
        d = Demonstrator.objects.get(pk=demonId)
        return render(request, 'home/insert-dispatch.html', {"d":d})


def getDispatch(request, dispatchId):
    ans = Dispatch.objects.get(pk = dispatchId)
    return render(request, 'home/show-dispatch.html', {'dispatch': ans})


def ReportInsert(request, dispatchId, demonId):
    
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                reportId = generalInsert(request, 'report', {'dispatchDecisionId': dispatchId}, Report, AddReport, savePoint)
                if type(reportId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التقرير")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة التقرير ")
            return redirect('app:home')
            
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')


def ExtensionInsert(request, dispatchId,demonId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                extensionId = generalInsert(request, 'extensionDecisionNumber', {'dispatchDecisionId': dispatchId}, Extension, AddExtension, savePoint)
                if type(extensionId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التمديد")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة التمديد ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'home/ext.html')


def FreezeInsert(request, dispatchId,demonId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                freezeId = generalInsert(request, 'freezeDecisionNumber', {'dispatchDecisionId': dispatchId}, Freeze, AddFreeze, savePoint)
                if type(freezeId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التجميد")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة التجميد ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
    else:
        return render(request, 'registration/dispathInsert.html')


def DurationChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'durationChangeDurationYear', {'dispatchDecisionId': dispatchId}, DurationChange, AddDurationChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير المدة")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير المدة ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


def AlimonyChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'newAlimony', {'dispatchDecisionId': dispatchId}, AlimonyChange, AddAlimonyChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير النفقة")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير النفقة ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


def UniversityChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'newUniversity', {'dispatchDecisionId': dispatchId}, UniversityChange, AddUniversityChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير الجامعة")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير الجامعة ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


def SpecializationChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'newSpecialization', {'dispatchDecisionId': dispatchId}, SpecializationChange, AddSpecializationChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير الاختصاص")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير الاختصاص ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


def getAllDemonstrators(request):
    data2 = serializers.serialize('json', Demonstrator.objects.all(), fields=('id', 'name', 'fatherName', 'motherName', 'college'))
    return render(request, 'home/allDemonstrators.html', {'result': data2})


def getDemonstrator(request, id):
    demonstrator = Demonstrator.objects.select_related().prefetch_related().all().get(pk=id)
    return render(request, 'home/demonstrator.html', {'demonstrator': demonstrator})
   

def generalUpdate(request, mainField, baseDic, model, addModel, obj, savePoint):
    try:
        id = None
        if mainField in request.POST:
            dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
            dic.update(baseDic)
            for field in model._meta.local_fields:
                if field.name in request.POST:
                    dic[field.name] = request.POST[field.name]
            form = addModel(dic, instance=obj)
            if form.is_valid():
                id = form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                return form.errors
        return id
    except:
        print('error')


def UpdateDemonstrator(request, id):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=id).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                demonstrators = Demonstrator.objects.filter(pk=id)
                for demonstrator in demonstrators:
                    demonId= generalUpdate(request, 'name', {}, Demonstrator, AddDemonstrator, demonstrator, savePoint)
                    if type(demonId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateUniversityDegree(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                universityDegrees= UniversityDegree.objects.filter(pk=id)
                for universityDegree in universityDegrees:
                    resId = generalUpdate(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, universityDegree, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateNomination(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                nominations= Nomination.objects.filter(pk=id)
                for nomination in nominations:
                    resId = generalUpdate(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, nomination, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateAdjectiveChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                adjectiveChange= AdjectiveChange.objects.filter(pk=id)
                for model in adjectiveChange:
                    resId = generalUpdate(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

                try:
                    if 'adjectiveChangeAdjective' in request.POST:
                        demonstrators= Demonstrator.objects.filter(pk=demonId)
                        for demonstrator in demonstrators:
                            demonstrator.currentAdjective = request.POST['adjectiveChangeAdjective']
                            Demonstrator.full_clean(self=demonstrator)
                            Demonstrator.save()
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateCertificateOfExcellence(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                certificateOfExcellence= CertificateOfExcellence.objects.filter(pk=id)
                for model in certificateOfExcellence:
                    resId = generalUpdate(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateGraduateStudies(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                graduateStudies= GraduateStudies.objects.filter(pk=id)
                for model in graduateStudies:
                    resId = generalUpdate(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateDispatch(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                dispatchs= Dispatch.objects.filter(pk=id)
                for dispatch in dispatchs:
                    dispatchId = generalUpdate(request, 'dispatchDecisionNumber', {'studentId': demonId}, Dispatch, AddDispatch, dispatch, savePoint)
                    if type(dispatchId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateReport(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                reports= Report.objects.filter(pk=id)
                for report in reports:
                    resId = generalUpdate(request, 'regularizationDecisionNumber', {'dispatchDecisionId': report.dispatchDecisionId}, Report, AddReport, report, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateRegularization(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                regularizations= Regularization.objects.filter(pk=id)
                for regularization in regularizations:
                    resId = generalUpdate(request, 'regularizationDecisionNumber', {'regularizationDecisionId': regularization.regularizationDecisionId}, Regularization, AddRegularization, regularization, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateExtension(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                extensions= Extension.objects.filter(pk=id)
                for extension in extensions:
                    extensionId = generalUpdate(request, 'extensionDecisionNumber', {'dispatchDecisionId': extension.dispatchDecisionId}, Extension, AddExtension, extension, savePoint)
                    if type(extensionId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateFreeze(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                freezes= Freeze.objects.filter(pk=id)
                for freeze in freezes:
                    freezeId = generalUpdate(request, 'freezeDecisionNumber', {'dispatchDecisionId': freeze.dispatchDecisionId}, Freeze, AddFreeze, freeze, savePoint)
                    if type(freezeId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateDurationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                durationChange= DurationChange.objects.filter(pk=id)
                for model in durationChange:
                    resId = generalUpdate(request, 'durationChangeDurationYear', {'dispatchDecisionId': model.dispatchDecisionId}, DurationChange, AddDurationChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateAlimonyChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                alimonyChange= AlimonyChange.objects.filter(pk=id)
                for model in alimonyChange:
                    resId = generalUpdate(request, 'newAlimony', {'dispatchDecisionId': model.dispatchDecisionId}, AlimonyChange, AddAlimonyChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateUniversityChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                universityChange= UniversityChange.objects.filter(pk=id)
                for model in universityChange:
                    resId = generalUpdate(request, 'newUniversity', {'dispatchDecisionId': model.dispatchDecisionId}, UniversityChange, AddUniversityChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


def UpdateSpecializationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                specializationChange= SpecializationChange.objects.filter(pk=id)
                for model in specializationChange:
                    resId = generalUpdate(request, 'newSpecialization', {'dispatchDecisionId': model.dispatchDecisionId}, SpecializationChange, AddSpecializationChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})
 

def QueryDemonstrator(request):
    if request.method == 'POST':

        def makeQuery(query, op):
            obj = Q()
            for item in query: 
                q = list(item.keys())[0]
                if type(item[q]) is list:
                    if op == 'or':
                        obj = obj | (makeQuery(item[q], q))
                    else:
                        obj = obj & (makeQuery(item[q], q))
                elif type(item[q]) is dict:
                    p = list (item[q].keys())[0]
                    if op == 'or':
                        obj = obj | Q(**{q+p: item[q][p]})
                    else:
                        obj = obj & Q(**{q+p: item[q][p]})
                else: 
                    if op == 'or':
                        obj = obj | Q(**{q: item[q]})
                    else: 
                        obj = obj & Q(**{q: item[q]})
            return obj

        query = request.POST['query']
        op = list(query.keys())[0]
        obj = makeQuery(query[op], op)
        result = serializers.serialize('json', Demonstrator.objects.filter(obj))
        print(result)
    
        return render(request, 'registration/result.html', {'result': result})



def home(request):
    return render(request, 'home/home.html')

def Test(request):
    date= request.user.lastPull.lastPullDate
    data=[]
    for model in apps.get_models():
        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull']:
            tempData =list( model.objects.filter(lastModifiedDate__gte=date) )
            data.append( {'modelName': model.__name__, 'data':tempData})
    return render(request, 'registration/result.html', {'result': 'done'})

def goToHome(request):
    return redirect('app:home')


def pullData(request):
    if request.method=='POST':
        if request.user.is_superuser:
             with transaction.atomic():
                savePoint= transaction.savepoint()
                try:
                    lastPullDate= request.user.lastPull.lastPullDate
                    data={}
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull']:
                            added = list (model.objects.filter(createdDate__gte=lastPullDate))
                            updated =list( model.objects.filter(Q(lastModifiedDate__gte=lastPullDate) & ~Q(createdDate__gte=lastPullDate) ) )
                            data.update( {model.__name__: {'updated':updated, 'added':added} })
                        LastPull.objects.filter(pk=1).update(lastPullDate=datetime.datetime.now)
                    return render(request, 'registration/result.html', {'result': 'done'})
                except:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': 'done'}) 
        else:
            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/result.html', {'result': 'done'})


def generalPushAdd(request ,added, addModel, savePoint):
    id = None
    dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
    dic.update(added)
    form = addModel(dic)
    if form.is_valid():
        id = form.save()
    else:
        transaction.savepoint_rollback(savePoint)
        return form.errors
    return id


def generalPushUpdate(request ,added, addModel, obj, savePoint):
    id = None
    dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
    dic.update(added)
    form = addModel(dic, instance=obj)
    if form.is_valid():
        id = form.save()
    else:
        transaction.savepoint_rollback(savePoint)
        return form.errors
    return id


def pushData(request, data):
    if request.method=='POST':
        if request.user.is_superuser:
             with transaction.atomic():
                savePoint= transaction.savepoint()
                try:
                    modelforms = forms.ModelForm.__subclasses__()
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull']:
                            addModel= filter(lambda x:x.Meta.model == model, modelforms)[0] 

                            # add
                            for added in data[model.__name__]['added']:
                                id = generalPushAdd(request, added , addModel, savePoint)
                                if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

                            # update
                            for updated in data[model.__name__]['updated']:
                                objs= model.objects.filter(pk=updated.id)
                                for obj in objs:
                                    id = generalPushUpdate(request, added , obj, addModel, savePoint)
                                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                                                 
                    return render(request, 'registration/result.html', {'result': 'done'})
                except:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': 'done'}) 
        else:
            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/result.html', {'result': 'done'})

def do_something(request):
        
        return render(request, "home/query.html")

def gett(request):
    data2 = serializers.serialize('json', Demonstrator.objects.select_related().prefetch_related().all())
    
    return JsonResponse(data2, safe=False)
