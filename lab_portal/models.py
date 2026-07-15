from django.db import models
from django.contrib.auth.models import User

class LabTicket(models.Model):
    # Restored your exact labs: Lab 1, SIIS Lab, and Multidisciplinary Lab
    LAB_ROOM_CHOICES = [
        ('LAB_1', 'Lab 1'),
        ('SIIS_LAB', 'SIIS Lab'),
        ('MULTIDISCIPLINARY', 'Multidisciplinary Lab'),
    ]

    CATEGORY_CHOICES = [
        ('HARDWARE', 'Hardware Fault (Keyboard, Mouse, Monitor, PC)'),
        ('SOFTWARE', 'Software & OS issues'),
        ('NETWORK', 'Network & Internet Connection issues'),
        ('POWER', 'Power & Electrical supply issues'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Assigned', 'Assigned to Technician'),
        ('Resolved', 'Resolved / Work Done'),
    ]

    lab_room = models.CharField(max_length=50, choices=LAB_ROOM_CHOICES)
    computer_number = models.CharField(max_length=50)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    student_email = models.EmailField(blank=True, null=True, help_text="Optional for status email updates")
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'is_staff': True})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.get_lab_room_display()} ({self.status})"
