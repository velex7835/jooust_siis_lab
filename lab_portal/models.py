from django.db import models
from django.contrib.auth.models import User

class LabTicket(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Assigned', 'Assigned to Technician'),
        ('Resolved', 'Resolved / Work Done'),
    ]

    lab_room = models.CharField(max_length=50)
    computer_number = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    description = models.TextField()
    
    # New IT Operations Fields
    student_email = models.EmailField(blank=True, null=True, help_text="Optional for status email updates")
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'is_staff': True})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.lab_room} ({self.status})"
