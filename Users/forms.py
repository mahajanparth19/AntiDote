from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User,Reports,Treatment,Doctor,Patient


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ['email']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['email']

class FileForm(forms.ModelForm):
    class Meta:
        model= Reports
        fields= ["name", "filepath","Description"]
    
    def save(self,user):
        data = self.cleaned_data
        report = Reports(name=data['name'], filepath=data['filepath'],
            Description=data['Description'], Patient=user.Patient)
        report.save()

class send_to_doc_Form(forms.ModelForm):
    class Meta:
        model= Reports
        fields = ["Doctors"]
    
#     def __init__ (self, *args, **kwargs,Patient):
#         Patient = self.Patient
#         super(send_to_doc_Form, self).__init__(*args, **kwargs)
#         self.fields["Doctors"].widget = forms.widgets.CheckboxSelectMultiple()
#         self.fields["Doctors"].queryset = Patient.Treatments.Doctors.all()
        

# class Treatment_Form(forms.ModelForm):
#     class Meta:
#         model= Treatment
#         fields = ["Doctor","Disease"]
    

class Register_Doc(forms.ModelForm):
    class Meta:
        model=Doctor
        exclude = ['user']


class Register_Patient(forms.ModelForm):
    class Meta:
        model=Patient
        exclude = ['user']