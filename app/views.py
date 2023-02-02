from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.utils import ErrorDict
from .models import *
from .forms import *
from django.core import serializers
from django.contrib import messages


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
            messages.add_message(
                request, messages.SUCCESS,
                "أهلاً و سهلاً")
            return redirect('app:home')
        else:
            return render(request, 'registration/result.html', {'result': 'no such a user'})

    return render(request, 'registration/login.html')


def Logout(request):
    logout(request)
    messages.add_message(
                request, messages.ERROR,
                "تم تسجيل الخروج")
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
        return render(request, 'home/insert.html')


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


def getAllDemonstrators(request):
    # data1 = Demonstrator.objects.all().values()
    data2 = serializers.serialize('json', Demonstrator.objects.all(), fields=('id', 'name', 'fatherName', 'motherName', 'college'))
    print(data2)
    return render(request, 'home/allDemonstrators.html', {'result': data2})

def getDemonstrator(request, id):
    demonstrator = Demonstrator.objects.filter(pk=id).values()
    
    print(demonstrator)
    return render(request, 'home/demonstrator.html', {'demonstrator': demonstrator[0]})

    

def generalUpdate(request, mainField, baseDic, model, addModel, obj, savePoint, i):
    try:
        id = None
        if mainField in request.POST:
            dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
            dic.update(baseDic)
            for field in model._meta.local_fields:
                if field.name in request.POST:
                    dic[field.name] = request.POST.getlist(field.name)[i]
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
    demonstrators = Demonstrator.objects.filter(pk=id)
    if request.method == 'POST':
        with transaction.atomic():
            savePoint= transaction.savepoint()

            for demonstrator in demonstrators:
                demonId= generalUpdate(request, 'name', {}, Demonstrator, AddDemonstrator, demonstrator, savePoint, 0)
                if type(demonId) == ErrorDict: return render(request, 'registration/result.html', {'result': demonId})

                nominations= Nomination.objects.filter(nominationDecision=demonId)
                for nomination in nominations:
                    id = generalUpdate(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, nomination, savePoint, 0)
                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

                universityDegrees= UniversityDegree.objects.filter(universityDegree=demonId)
                for universityDegree in universityDegrees:
                    id = generalUpdate(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, universityDegree, savePoint, 0)
                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})

                graduateStudiesCount= 0 
                graduateStudies= GraduateStudies.objects.filter(studentId=demonId)
                for model in graduateStudies:
                    id = generalUpdate(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, model, savePoint, graduateStudiesCount)
                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                    graduateStudiesCount+= 1

                certificateOfExcellenceCount= 0
                certificateOfExcellence= CertificateOfExcellence.objects.filter(studentId=demonId)
                for model in certificateOfExcellence:
                    id = generalUpdate(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, model, savePoint, certificateOfExcellenceCount)
                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                    certificateOfExcellenceCount+= 1

                adjectiveChangeCount= 0
                adjectiveChange= AdjectiveChange.objects.filter(studentId=demonId)
                for model in adjectiveChange:
                    id = generalUpdate(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, model, savePoint, adjectiveChangeCount)
                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                    adjectiveChangeCount+= 1
                    if 'adjectiveChangeAdjective' in request.POST:
                        demonstrator.currentAdjective = request.POST['adjectiveChangeAdjective']
                        Demonstrator.full_clean(self=demonstrator)
                        Demonstrator.save()

                dispatchCount= 0
                regularizationCount= 0
                extensionCount= 0
                freezeCount= 0
                durationCount= 0
                dispatchs= Dispatch.objects.filter(studentId=demonId)
                for dispatch in dispatchs:
                    dispatchId = generalUpdate(request, 'dispatchDecisionNumber', {'studentId': demonId}, Dispatch, AddDispatch, dispatch, savePoint, dispatchCount)
                    if type(dispatchId) == ErrorDict: return render(request, 'registration/result.html', {'result': dispatchId})

                    regularizations= Regularization.objects.filter(regularizationDecisionId=dispatchId)
                    for regularization in regularizations:
                        id = generalUpdate(request, 'regularizationDecisionNumber', {'regularizationDecisionId': dispatchId}, Regularization, AddRegularization, regularization, savePoint, regularizationCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        regularizationCount+= 1

                    dispatchDurations= Duration.objects.filter(dispatchDuration=dispatchId)
                    for dispatchDuration in dispatchDurations:
                        id = generalUpdate(request, 'durationYear', {'dispatchDuration': dispatchId}, Duration, AddDuration, dispatchDuration, savePoint, durationCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        durationCount+= 1

                    languageCourseDurations= Duration.objects.filter(languageCourseDuration=dispatchId)
                    for languageCourseDuration in languageCourseDurations:
                        id = generalUpdate(request, 'durationYear', {'languageCourseDuration': dispatchId}, Duration, AddDuration, languageCourseDuration, savePoint, durationCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        durationCount+= 1

                    alimonyChangeCount= 0
                    alimonyChange= AlimonyChange.objects.filter(dispatchDecisionId=dispatchId)
                    for model in alimonyChange:
                        id = generalInsert(request, 'newAlimony', {'dispatchDecisionId': dispatchId}, AlimonyChange, AddAlimonyChange, model, savePoint, alimonyChangeCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        alimonyChangeCount+= 1

                    universityChangeCount= 0
                    universityChange= UniversityChange.objects.filter(dispatchDecisionId=dispatchId)
                    for model in universityChange:
                        id = generalInsert(request, 'newUniversity', {'dispatchDecisionId': dispatchId}, UniversityChange, AddUniversityChange, model, savePoint, universityChangeCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        universityChangeCount+= 1

                    specializationChangeCount= 0
                    specializationChange= SpecializationChange.objects.filter(dispatchDecisionId=dispatchId)
                    for model in specializationChange:
                        id = generalInsert(request, 'newSpecialization', {'dispatchDecisionId': dispatchId}, SpecializationChange, AddSpecializationChange, model, savePoint, specializationChangeCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        specializationChangeCount+= 1


                        # heeeeeeeeeeeeeeeeeeeeeeeeeeere

                    durationChanges= DurationChange.objects.filter(dispatchDecisionId=dispatchId)
                    for durationChange in durationChanges:
                        durationChangeId= durationChange.id
                        durationObject = Duration.objects.filter(newDuration=durationChangeId)
                        for obj in durationObject:
                            id = generalUpdate(request, 'durationYear', {'newDuration': durationChangeId}, Duration, AddDuration, durationObject, savePoint, durationCount)
                            if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                            durationCount+= 1

 
                    extensions= Extension.objects.filter(dispatchDecisionId=dispatchId)
                    for extension in extensions:
                        extensionId = generalUpdate(request, 'extensionDecisionNumber', {'dispatchDecisionId': dispatchId}, Extension, AddExtension, extension, savePoint, extensionCount)
                        if type(extensionId) == ErrorDict: return render(request, 'registration/result.html', {'result': extensionId})

                        extensionDuration= Duration.objects.filter(extensionDuration=extensionId)
                        id = generalUpdate(request, 'durationYear', {'extensionDuration': extensionId}, Duration, AddDuration, extensionDuration, savePoint, durationCount)
                        if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                        durationCount+= 1


                        freezes= Freeze.objects.filter(extensionDecisionId=extensionId)
                        for freeze in freezes:
                            freezeId = generalUpdate(request, 'freezeDecisionNumber', {'extensionDecisionId': extensionId}, Freeze, AddFreeze, freeze, savePoint, freezeCount)
                            if type(freezeId) == ErrorDict: return render(request, 'registration/result.html', {'result': freezeId})

                            freezeDurations= Duration.objects.filter(freezeDuration=freezeId)
                            for freezeDuration in freezeDurations:
                                id = generalUpdate(request, 'durationYear', {'freezeDuration': freezeId}, Duration, AddDuration, freezeDuration, savePoint, durationCount)
                                if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                                durationCount+= 1

                            freezeCount+= 1
                            

                        extensionCount+= 1
      

                    dispatchCount+= 1


        return render(request, 'registration/result.html', {'result': 'done'})

    else:
        return render(request, 'registration/update.html', {'form': demonstrators})
   

def QueryDemonstrator(request):
    if request.method=='POST':
        keysList= list(request.POST.keys())
        keysList.pop(0)
        result = Demonstrator.objects.filter(**{fieldName: request.POST[fieldName] for fieldName in keysList if request.POST[fieldName] != ""} )
        print(result)
    
    return render(request, 'home/query.html')


def home(request):
    return render(request, 'home/home.html')