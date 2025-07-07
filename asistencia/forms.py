from .models import Usuario
from django import forms

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(render_value=True),
        required=False
    )

    class Meta:
        model = Usuario
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.rol:
            self.fields['rol'].initial = 'usuario'
        # Si es edición, el password no es obligatorio
        if self.instance.pk:
            self.fields['password'].required = False
        else:
            self.fields['password'].required = True
        # Agregar clases Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        elif not self.instance.pk:
            # Si es creación y no hay password, error
            raise forms.ValidationError('La contraseña es obligatoria.')
        if commit:
            user.save()
        return user

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

