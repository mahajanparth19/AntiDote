from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Patient


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Patient
        fields = ['email','Name','Age','Address','Gender']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Patient
        fields = ['email','Name','Age','Address','Gender']