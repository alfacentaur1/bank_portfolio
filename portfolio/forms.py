from django import forms
from .models import Integration

class IntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = ['source_app', 'target_app', 'integration_type', 'direction', 'data_volume', 'data_sensitivity']
        widgets = {
            # Tailwind styling pro formulář
            'source_app': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'target_app': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'integration_type': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'např. REST API'}),
            'direction': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Inbound/Outbound'}),
            'data_volume': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'např. 1k/day'}),
            'data_sensitivity': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'GDPR/Internal'}),
        }