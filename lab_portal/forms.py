from django import forms
from .models import LabTicket

class LabTicketForm(forms.ModelForm):
    class Meta:
        model = LabTicket
        fields = ['lab_room', 'computer_number', 'category', 'description']
        widgets = {
            'lab_room': forms.Select(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'
            }),
            'computer_number': forms.TextInput(attrs={
                'placeholder': 'e.g. COMP-04',
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe what is wrong with the machine or equipment...',
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'
            }),
        }
