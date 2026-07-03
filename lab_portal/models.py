from django.db import models

class LabTicket(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    CATEGORY_CHOICES = [
        ('Hardware', 'Hardware Failure (Mouse, Keyboard, Screen)'),
        ('Software', 'Software/OS Issue (Crashing, Missing Apps)'),
        ('Network', 'Network/Internet Disconnection'),
        ('Staff Complain', 'Staff/Lab Assistance Complaint'),
    ]

    LAB_CHOICES = [
        ('SIIS Lab', 'SIIS Lab'),
        ('Computer Lab 1', 'Computer Lab 1'),
        ('Multidisciplinary Lab', 'Multidisciplinary Lab'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    reg_number_or_staff_id = models.CharField(max_length=50)
    lab_room = models.CharField(max_length=30, choices=LAB_CHOICES)
    computer_number = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} on {self.computer_number} [{self.status}]"
