from django import forms
from .models import Propuesta

class PropuestaForm(forms.ModelForm):
    class Meta:
        model = Propuesta
        fields = ['nombre', 'tema']

class PropuestaEditForm(forms.ModelForm):
    class Meta:
        model = Propuesta
        fields = ['nombre', 'tema']