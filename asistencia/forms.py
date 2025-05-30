#esto es para cuando ya este el models.py y para agregar en los views

from django import forms
from .models import usuario


class usuarioForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = "__all__"

class LoginForm(forms.Form):  # antes: forms.form
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "nombre / correo", "class": "login_input"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "login_input"}
        )
    )
