from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.utils import ErrorDict
from .models import *
from .forms import *


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


def generalInsert(request, mainField, baseDic, model, addModel, savePoint):
    id = None
    for i in range(len(request.POST.getlist(mainField))):
        dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
        dic.update(baseDic)
        for field in model._meta.local_fields:
            print(field.name)
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
        with transaction.atomic():
            savePoint = transaction.savepoint()

            demonId = generalInsert(request, 'name', {}, Demonstrator, AddDemonstrator, savePoint)
            if type(demonId) == ErrorDict: return render(request, 'registration/result.html', {'result': demonId})

            id = generalInsert(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            id = generalInsert(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            id = generalInsert(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            id = generalInsert(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

        return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/insert.html')


def AdjectiveChangeInsert(request, demonId):
    if request.method == 'POST':
        with transaction.atomic():
            savePoint = transaction.savepoint()

            id = generalInsert(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            demonstrator = Demonstrator.objects.get(pk=demonId)
            demonstrator.currentAdjective = request.POST['adjectiveChangeAdjective']
            Demonstrator.full_clean(self=demonstrator)
            Demonstrator.save()

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def DispatchInsert(request, demonId):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint = transaction.savepoint()

            dispatchId = generalInsert(request, 'dispatchDecisionNumber', {'studentId': demonId}, Dispatch, AddDispatch, savePoint)
            if type(dispatchId) == ErrorDict: return render(request, 'registration/result.html', {'result': dispatchId})

            id = generalInsert(request, 'regularizationDecisionNumber', {'regularizationDecisionId': dispatchId}, Regularization, AddRegularization, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            id = generalInsert(request, 'durationYear', {'dispatchDuration': dispatchId}, Duration, AddDuration, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            id = generalInsert(request, 'durationYear', {'languageCourseDuration': dispatchId}, Duration, AddDuration, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def ExtensionInsert(request, dispatchId):
    if request.method == 'POST':
        with transaction.atomic():
            savePoint = transaction.savepoint()

            extensionId = generalInsert(request, 'extensionDecisionNumber', {'dispatchDecisionId': dispatchId}, Extension, AddExtension, savePoint)
            if type(extensionId) == ErrorDict: return render(request, 'registration/result.html', {'result': extensionId})

            id = generalInsert(request, 'durationYear', {'extensionDuration': extensionId}, Duration, AddDuration, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def FreezeInsert(request, extensionId):
    if request.method == 'POST':
        with transaction.atomic():
            savePoint = transaction.savepoint()

            freezeId = generalInsert(request, 'freezeDecisionNumber', {'extensionDecisionId': extensionId}, Freeze, AddFreeze, savePoint)
            if type(freezeId) == ErrorDict: return render(request, 'registration/result.html', {'result': freezeId})

            id = generalInsert(request, 'durationYear', {'freezeDuration': freezeId}, Duration, AddDuration, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def DurationChangeInsert(request, dispatchId):
    if request.method == 'POST':
        with transaction.atomic():

            savePoint = transaction.savepoint()
            durationDhangeId = None

            dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'], 'dispatchDecisionId': dispatchId}
            form = AddDurationChange(dic)
            if form.is_valid():
                durationDhangeId = form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                return render(request, 'registration/result.html', {'result': form.errors})

            id = generalInsert(request, 'durationYear', {'newDuration': durationDhangeId}, Duration, AddDuration, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def AlimonyChangeInsert(request, dispatchId):
    if request.method == 'POST':
        with transaction.atomic():
            savePoint = transaction.savepoint()

            id = generalInsert(request, 'newAlimony', {'dispatchDecisionId': dispatchId}, AlimonyChange, AddAlimonyChange, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def UniversityChangeInsert(request, dispatchId):
    if request.method == 'POST':
        with transaction.atomic():
            savePoint = transaction.savepoint()

            id = generalInsert(request, 'newUniversity', {'dispatchDecisionId': dispatchId}, UniversityChange, AddUniversityChange, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def SpecializationChangeInsert(request, dispatchId):
    if request.method == 'POST':
        with transaction.atomic():
            savePoint = transaction.savepoint()

            id = generalInsert(request, 'newSpecialization', {'dispatchDecisionId': dispatchId}, SpecializationChange, AddSpecializationChange, savePoint)
            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/dispathInsert.html')


def UpdateDemonstrator(request, id):
    demonstrator = Demonstrator.objects.get(pk=id)
    if request.method == 'POST':
        form = AddDemonstrator(request.POST, instance=demonstrator)

    else:
        return render(request, 'registration/insert2.html', {'form': demonstrator})
