from django.db import models
from app.constantVariables import *
from django.contrib.auth.models import User
import datetime


class LastPull(models.Model):
    userId= models.OneToOneField(User,on_delete=models.CASCADE, related_name='lastPull', blank=True)
    lastPullDate= models.DateTimeField(default=datetime.datetime(2000, 5, 12))


class Permissions(models.Model):
    userId= models.ManyToManyField(User, related_name='permissions', blank=True)
    permissionsCollege = models.CharField(max_length=100, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Demonstrator(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    fatherName = models.CharField(max_length=50, null=True, blank=True)
    motherName = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    home = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=25, validators=[
                              MOBILE_NUMBER_VALIDATOR], null=True, blank=True)
    telephone = models.CharField(max_length=25, validators=[
                                 TELEPHONE_VALIDATOR], null=True, blank=True)
    maritalStatus = models.CharField(
        max_length=10, choices=MARITAL_CHOICES, null=True, blank=True)
    militarySituation = models.CharField(
        max_length=25, choices=MILITARY_SITUATION_CHOICES, null=True, blank=True)
    residence = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    currentAdjective = models.CharField(
        max_length=50, choices=ADJECTIVE_CHOICES, null=True, blank=True, default='demonstrator')
    nominationReason = models.CharField(
        max_length=25, choices=NOMINATION_REASON_CHOICES, null=True, blank=True)
    contestAnnouncementDate = models.DateField(null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=100, null=True, blank=True)
    secion = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    commencementAfterNominationDate = models.DateField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.fatherName} son of {self.motherName  }'


class UniversityDegree(models.Model):
    universityDegree = models.OneToOneField(Demonstrator, on_delete=models.CASCADE,
                                            primary_key=True, related_name='universityDegree', default=0)
    universityDegreeUniversity = models.CharField(
        max_length=100, null=True, blank=True)
    universityDegreeCollege = models.CharField(
        max_length=100, null=True, blank=True)
    universityDegreeSection = models.CharField(
        max_length=100, null=True, blank=True)
    universityDegreeYear = models.CharField(max_length=10, validators=[
        YEAR_VALIDATOR], null=True, blank=True)
    universityDegreeAverage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Nomination(models.Model):
    nominationDecision = models.OneToOneField(
        Demonstrator, on_delete=models.CASCADE, primary_key=True, related_name='nominationDecision', default=0)
    nominationDecisionNumber = models.IntegerField(null=True, blank=True)
    nominationDecisionDate = models.DateField(null=True, blank=True)
    nominationDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class AdjectiveChange(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='adjectiveChange', null=True, blank=True)
    adjectiveChangeDecisionNumber = models.IntegerField(null=True, blank=True)
    adjectiveChangeDecisionDate = models.DateField(null=True, blank=True)
    adjectiveChangeDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES, null=True, blank=True)
    adjectiveChangeAdjective = models.CharField(
        max_length=50, choices=ADJECTIVE_CHOICES, null=True, blank=True)
    adjectiveChangeReason = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class CertificateOfExcellence(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='certificateOfExcellence', null=True, blank=True)
    certificateOfExcellenceYear = models.CharField(
        max_length=1, choices=EXCELLENCE_YEAR_CHOICES, null=True, blank=True)
    certificateOfExcellenceDegree = models.CharField(
        max_length=1, choices=EXCELLENCE_DEGREE_CHOICES, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class GraduateStudies(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='graduateStudies', null=True, blank=True)
    graduateStudiesDegree = models.CharField(
        max_length=10, choices=GRADUATE_STUDIES_DEGREE_CHOICES, null=True, blank=True)
    graduateStudiesUniversity = models.CharField(
        max_length=100, null=True, blank=True)
    graduateStudiesCollege = models.CharField(
        max_length=100, null=True, blank=True)
    graduateStudiesSection = models.CharField(
        max_length=100, null=True, blank=True)
    graduateStudiesSpecialzaion = models.CharField(
        max_length=100, null=True, blank=True)
    graduateStudiesYear = models.CharField(max_length=10, validators=[
        YEAR_VALIDATOR], null=True, blank=True)
    graduateStudiesAverage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Dispatch(models.Model):

    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='dispatch', null=True, blank=True)
    dispatchDecisionNumber = models.IntegerField(null=True, blank=True)
    dispatchDecisionDate = models.DateField(null=True, blank=True)
    dispatchDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES, null=True, blank=True)
    requiredCertificate = models.CharField(
        max_length=10, choices=CERTIFICATE_TYPE, null=True, blank=True)
    dispatchType = models.CharField(
        max_length=10, choices=DISPATCH_TYPE, null=True, blank=True)
    alimony = models.CharField(
        max_length=25, choices=ALIMONY, null=True, blank=True)
    dispatchCountry = models.CharField(max_length=100, null=True, blank=True)
    dispatchUniversity = models.CharField(
        max_length=100, null=True, blank=True)
    dispatchDurationYear = models.IntegerField(null=True, blank=True)
    dispatchDurationMonth = models.IntegerField(null=True, blank=True)
    dispatchDurationDay = models.IntegerField(null=True, blank=True)
    languageCourseDurationYear = models.IntegerField(null=True, blank=True)
    languageCourseDurationMonth = models.IntegerField(null=True, blank=True)
    languageCourseDurationDay = models.IntegerField(null=True, blank=True)
    dispatchEndDate = models.DateField(null=True, blank=True)
    backDate = models.DateField(null=True, blank=True)
    innerSupervisor = models.CharField(max_length=50, null=True, blank=True)
    outerSupervisor = models.CharField(max_length=50, null=True, blank=True)
    defenseDate = models.DateField(null=True, blank=True)
    gettingCertificateDate = models.DateField(null=True, blank=True)
    commencementDate = models.DateField(null=True, blank=True)
    atDisposalOfUniversityDate = models.DateField(null=True, blank=True)
    dispatchNotes = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Report(models.Model):
    dispatchDecisionId = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='report', null=True, blank=True)
    report = models.TextField(null=True, blank=True)
    reportDate = models.DateField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Regularization(models.Model):
    regularizationDecisionId = models.OneToOneField(
        Dispatch, on_delete=models.CASCADE, primary_key=True, related_name='regularization', default=0)
    regularizationDecisionNumber = models.IntegerField(null=True, blank=True)
    regularizationDecisionDate = models.DateField(null=True, blank=True)
    regularizationDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES, null=True, blank=True)
    regularizationDecisionNotes = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Extension(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='extension', null=True, blank=True)
    extensionDecisionNumber = models.IntegerField(null=True, blank=True)
    extensionDecisionDate = models.DateField(null=True, blank=True)
    extensionDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES, null=True, blank=True)
    extensionDurationYear = models.IntegerField(null=True, blank=True)
    extensionDurationMonth = models.IntegerField(null=True, blank=True)
    extensionDurationDay = models.IntegerField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class Freeze(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='freeze', null=True, blank=True)
    freezeDecisionNumber = models.IntegerField(null=True, blank=True)
    freezeDecisionDate = models.DateField(null=True, blank=True)
    freezeDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES, null=True, blank=True)
    freezeDurationYear = models.IntegerField(null=True, blank=True)
    freezeDurationMonth = models.IntegerField(null=True, blank=True)
    freezeDurationDay = models.IntegerField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class DurationChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='durationChange', null=True, blank=True)
    durationChangeDurationYear = models.IntegerField(null=True, blank=True)
    durationChangeDurationMonth = models.IntegerField(null=True, blank=True)
    durationChangeDurationDay = models.IntegerField(null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class AlimonyChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='alimonyChange', null=True, blank=True)
    newAlimony = models.CharField(
        max_length=25, choices=ALIMONY, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class UniversityChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='universityChange', null=True, blank=True)
    newUniversity = models.CharField(max_length=100, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)


class SpecializationChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='specializationChange', null=True, blank=True)
    newSpecialization = models.CharField(max_length=100, null=True, blank=True)
    createdDate = models.DateTimeField(default=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)

