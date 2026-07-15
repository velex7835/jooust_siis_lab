from django import forms
from .models import LabTicket

class LabTicketForm(forms.ModelForm):
    class Meta:
        model = LabTicket
        fields = ['lab_room', 'computer_number', 'category', 'description', 'screenshot', 'student_email']
        widgets = {
            'lab_room': forms.Select(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'computer_number': forms.TextInput(attrs={'placeholder': 'e.g. COMP-04', 'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'category': forms.Select(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe what is wrong...', 'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'screenshot': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none p-2'}),
            'student_email': forms.EmailInput(attrs={'placeholder': 'your-email@student.jooust.ac.ke (Optional)', 'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        }
