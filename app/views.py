from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import*
from .forms import*

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
            return render(request, 'registration/result.html', {'result': 'registeration success'})
        else:
            return render(request, 'registration/result.html', {'result': 'denied'})

    if request.user.is_superuser:
        return render(request, 'registration/register.html')
    else:
        return render(request, 'registration/result.html', {'result': 'denied'})


def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'registration/result.html', {'result': 'admin' if request.user.is_superuser else 'user'})
        else:
            return render(request, 'registration/result.html', {'result': 'no such a user'})

    return render(request, 'registration/login.html')


def Logout(request):
    logout(request)
    return redirect('app:login')


def DemonstratorInsert2(request):
    if request.method == 'POST':

        with transaction.atomic():

            savePoint= transaction.savepoint()
            demonId= None

            if 'name' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken']}
                for field in Demonstrator._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddDemonstrator(dic)
                if form.is_valid():
                    demonId=form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'nominationDecisionNumber' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'nominationDecision': demonId}
                for field in Nomination._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddNomination(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'universityDegreeUniversity' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'universityDegree': demonId}
                for field in UniversityDegree._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddUniversityDegree(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            
            for i in range(len(request.POST.getlist('graduateStudiesDegree'))):
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'studentId':demonId}
                for field in GraduateStudies._meta.local_fields:
                    if field.name in request.POST:
                        dic[field.name]=request.POST.getlist(field.name)[i]
                form = AddGraduateStudies(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})
            
            for i in range(len(request.POST.getlist('certificateOfExcellenceYear'))):
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'studentId':demonId}
                for field in CertificateOfExcellence._meta.local_fields:
                    if field.name in request.POST:
                        dic[field.name]=request.POST.getlist(field.name)[i]
                form = AddCertificateOfExcellence(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/insert.html')


def AdjectiveChangeInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            demonId= None

            if 'adjectiveChangeDecisionNumber' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'studentId': demonId}
                for field in AdjectiveChange._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddAdjectiveChange(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})
            
            demonstrator=Demonstrator.objects.get(pk=demonId)
            demonstrator.currentAdjective=request.POST['adjectiveChangeAdjective']
            Demonstrator.full_clean(self=demonstrator)
            Demonstrator.save()

            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def DispatchInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            demonId= None
            dispatchId=None

            if 'dispatchDecisionNumber' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'studentId': demonId}
                for field in Dispatch._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddDispatch(dic)
                if form.is_valid():
                    dispatchId=form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'regularizationDecisionNumber' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'regularizationDecisionId': dispatchId}
                for field in Regularization._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddRegularization(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'durationYear' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'dispatchDuration': dispatchId}
                for field in Duration._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST.getlist(field.name)[0]
                form = AddDuration(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'durationYear' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'languageCourseDuration': dispatchId}
                for field in Duration._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST.getlist(field.name)[0]
                form = AddDuration(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def ExtensionInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            dispatchId= None
            extensionId=None

            if 'extensionDecisionNumber' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'dispatchDecisionId': dispatchId}
                for field in Extension._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddExtension(dic)
                if form.is_valid():
                    extensionId= form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'durationYear' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'extensionDuration': extensionId}
                for field in Duration._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddDuration(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def FreezeInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            extensionId= None
            freezeId=None

            if 'extensionDecisionNumber' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'extensionDecisionId': extensionId}
                for field in Freeze._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddFreeze(dic)
                if form.is_valid():
                    freezeId= form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})

            if 'durationYear' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'freezeDuration': freezeId}
                for field in Duration._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddDuration(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})


            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def DurationChangeInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            dispatchId= None
            durationDhangeId=None

            dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'dispatchDecisionId': dispatchId}
            form = AddDurationChange(dic)
            if form.is_valid():
                durationDhangeId= form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                return render(request, 'registration/result.html', {'result': form.errors})

            if 'durationYear' in request.POST:
                dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'newDuration': durationDhangeId}
                for field in Duration._meta.local_fields:
                    if field.name in request.POST:
                            dic[field.name]=request.POST[field.name]
                form = AddDuration(dic)
                if form.is_valid():
                    form.save()
                else:
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': form.errors})


            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def AlimonyChangeInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            dispatchId= None

            dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'dispatchDecisionId': dispatchId, 'newAlimony': request.POST['newAlimony']}
            form = AddAlimonyChange(dic)
            if form.is_valid():
                form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                return render(request, 'registration/result.html', {'result': form.errors})
 
            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def UniversityChangeInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            dispatchId= None

            dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'dispatchDecisionId': dispatchId, 'newUniversity': request.POST['newUniversity']}
            form = AddUniversityChange(dic)
            if form.is_valid():
                form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                return render(request, 'registration/result.html', {'result': form.errors})
 
            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')


def SpecializationChangeInsert(request):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint= transaction.savepoint()
            dispatchId= None

            dic={'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken'], 'dispatchDecisionId': dispatchId, 'newSpecialization': request.POST['newSpecialization']}
            form = AddSpecializationChange(dic)
            if form.is_valid():
                form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                return render(request, 'registration/result.html', {'result': form.errors})
 
            return render(request, 'registration/result.html', {'result': 'done'})      
    else:
        return render(request, 'registration/dispathInsert.html')