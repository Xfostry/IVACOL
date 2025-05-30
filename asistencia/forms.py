from .models import usuario
from django import forms


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
