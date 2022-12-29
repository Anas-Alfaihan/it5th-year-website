
from django.forms import ModelForm
from .models import*

class AddDemonstrator(ModelForm):
    class Meta:
        model = Demonstrator
        exclude = []

class AddUniversityDegree(ModelForm):
    class Meta:
        model = UniversityDegree
        exclude = []

class AddNomination(ModelForm):
    class Meta:
        model = Nomination
        exclude = []

class AddAdjectiveChange(ModelForm):
    class Meta:
        model = AdjectiveChange
        exclude = []

class AddCertificateOfExcellence(ModelForm):
    class Meta:
        model = CertificateOfExcellence
        exclude = []

class AddGraduateStudies(ModelForm):
    class Meta:
        model = GraduateStudies
        exclude = []

class AddDispatch(ModelForm):
    class Meta:
        model = Dispatch
        exclude = []

class AddRegularization(ModelForm):
    class Meta:
        model = Regularization
        exclude = []

class AddExtension(ModelForm):
    class Meta:
        model = Extension
        exclude = []

class AddFreeze(ModelForm):
    class Meta:
        model = Freeze
        exclude = []

class AddDurationChange(ModelForm):
    class Meta:
        model = DurationChange
        exclude = []

class AddAlimonyChange(ModelForm):
    class Meta:
        model = AlimonyChange
        exclude = []

class AddUniversityChange(ModelForm):
    class Meta:
        model = UniversityChange
        exclude = []

class AddSpecializationChange(ModelForm):
    class Meta:
        model = SpecializationChange
        exclude = []

class AddDuration(ModelForm):
    class Meta:
        model = Duration
        exclude = []


