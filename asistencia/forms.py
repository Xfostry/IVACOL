from .models import Usuario
from django import forms

class UsuarioForm(forms.ModelForm):
    TIPO_DOCUMENTO_CHOICES = [
        ("CC", "Cédula de Ciudadanía (CC)"),
        ("CE", "Cédula de Extranjería (CE)"),
        ("PEP", "Permiso Especial de Permanencia (PEP)"),
        ("PPT", "Permiso por Protección Temporal (PPT)"),
        ("RUT", "Registro Único Tributario (RUT)"),
        ("NIT", "Número de Identificación Tributaria (NIT)")
    ]
    GENERO_CHOICES = [
        ("masculino", "Masculino"),
        ("femenino", "Femenino"),
        ("otro", "Otro"),
        ("no_especificado", "Prefiero no decir")
    ]
    CIUDAD_CHOICES = [
        ("bogota", "Bogotá"), ("medellin", "Medellín"), ("cali", "Cali"), ("barranquilla", "Barranquilla"),
        ("cartagena", "Cartagena"), ("cucuta", "Cúcuta"), ("bucaramanga", "Bucaramanga"), ("pereira", "Pereira"),
        ("santa_marta", "Santa Marta"), ("ibague", "Ibagué"), ("manizales", "Manizales"), ("neiva", "Neiva"),
        ("villavicencio", "Villavicencio"), ("pasto", "Pasto"), ("monteria", "Montería"), ("valledupar", "Valledupar"),
        ("armenia", "Armenia"), ("popayan", "Popayán"), ("sincelejo", "Sincelejo"), ("tunja", "Tunja"),
        ("florencia", "Florencia"), ("quibdo", "Quibdó"), ("riohacha", "Riohacha"), ("yopal", "Yopal"),
        ("mocoa", "Mocoa"), ("san_andres", "San Andrés"), ("leticia", "Leticia"), ("inírida", "Inírida"),
        ("mitu", "Mitú"), ("puerto_carreño", "Puerto Carreño")
    ]

    tipo_documento = forms.ChoiceField(choices=TIPO_DOCUMENTO_CHOICES, widget=forms.Select, required=True)
    genero = forms.ChoiceField(choices=GENERO_CHOICES, widget=forms.Select, required=True)
    ciudad = forms.ChoiceField(choices=CIUDAD_CHOICES, widget=forms.Select, required=True)
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(render_value=True),
        required=False
    )

    class Meta:
        model = Usuario
        # Solo los campos editables por el admin
        fields = [
            'first_name', 'last_name', 'tipo_documento', 'numero_documento', 'genero',
            'ciudad', 'telefono', 'direccion', 'rol', 'email', 'password'
        ]

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

