from dataclasses import Field
from django import forms
from .models import Borehole, Orphan, Report

class BoreholeForm(forms.ModelForm):
    class Meta:
        model = Borehole
        fields = ['borehole_id', 'local_government', 'Address', 'status', 'installed_date'] 

class RoleLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
class OrphanForm(forms.ModelForm):
    class Meta:
        model = Orphan
        fields = '__all__'

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'