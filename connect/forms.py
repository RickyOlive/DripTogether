from django import forms
from .models import Request, Connection


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'

class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'