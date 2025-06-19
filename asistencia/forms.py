from .models import Usuario
from django import forms

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Correo", "class": "login_input"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "login_input"}
        )
    )

