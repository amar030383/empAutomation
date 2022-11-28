from django.forms import ModelForm
from .models import UpgradeData
from django import forms

class UpgradeDataForm(ModelForm):
    device_Password = forms.CharField(widget=forms.PasswordInput)
    enable_Password = forms.CharField(widget=forms.PasswordInput)
    tFTP_Password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UpgradeData
       
        fields = '__all__'