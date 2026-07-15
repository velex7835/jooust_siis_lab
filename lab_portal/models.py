from django.db import models
from django.contrib.auth.models import User

class LabTicket(models.Model):
    # Fixed: Added official choices for the Lab selection fields
    LAB_ROOM_CHOICES = [
        ('SIIS_LAB_1', 'SIIS Lab 1 (Ground Floor)'),
        ('SIIS_LAB_2', 'SIIS Lab 2 (First Floor)'),
        ('SIIS_POSTGRAD', 'SIIS PostGrad Lab'),
        ('MAIN_LIBRARY_LAB', 'Main Library Computer Lab'),
    ]

    CATEGORY_CHOICES = [
        ('HARDWARE', 'Hardware Fault (Monitor, Mouse, Keyboard, PC)'),
        ('SOFTWARE', 'Software Issue (OS Crash, Missing Apps, Activation)'),
        ('NETWORK', 'Network & Internet Connectivity Outage'),
        ('POWER', 'Power Supply & UPS Failure'),
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
