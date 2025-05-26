#esto es para cuando ya este el models.py y para agregar en los views

from django import forms
from .models import estudiante


class estudianteForm(forms.ModelForm):
    class Meta:
        model = estudiante
        fields = '__all__'


class LoginForms(forms.form):
    username = forms.CharField (widget=forms.TextInput(attrs={"placeholder": "nombre / correo", "class": "login_input"}))
    
    password = forms.CharField (widget=forms.PasswordInput(attrs={"placeholder": "Pasword", "class": "login_input"}))

