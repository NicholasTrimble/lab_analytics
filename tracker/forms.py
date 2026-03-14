from django import forms
from .models import QualityTicket

class TicketForm(forms.ModelForm):
    class Meta:
        model = QualityTicket
        fields = ['doctor', 'department', 'issue_description', 'status']
        widgets = {
            'doctor': forms.Select(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px;'}),
            'department': forms.Select(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px;'}),
            'issue_description': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px;', 'placeholder': 'e.g., Short Margin'}),
            'status': forms.Select(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 15px;'}),
        }