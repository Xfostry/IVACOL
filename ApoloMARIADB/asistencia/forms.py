from django import forms
from .models import estudiante

class estudianteForm(forms.ModelForm):
    class Meta:
        model = estudiante
        fields = '__all__'