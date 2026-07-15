from django.contrib import admin
from django.core.mail import send_mail
from .models import LabTicket

@admin.register(LabTicket)
class LabTicketAdmin(admin.ModelAdmin):
    list_display = ('lab_room', 'computer_number', 'category', 'status', 'assigned_technician', 'created_at')
    list_filter = ('status', 'lab_room', 'assigned_technician')
    search_fields = ('computer_number', 'description')
    list_editable = ('status', 'assigned_technician')

    def save_model(self, request, obj, form, change):
        if change and obj.status == 'Resolved' and obj.student_email:
            old_obj = LabTicket.objects.get(pk=obj.pk)
            if old_obj.status != 'Resolved':
                send_mail(
                    subject=f"JOOUST SIIS Lab Ticket Resolved: {obj.computer_number}",
                    message=f"Hello,\n\nThe technical issue you reported regarding {obj.computer_number} in {obj.lab_room} has been marked as RESOLVED by our IT technicians.\n\nThank you for utilizing the JOOUST SIIS Lab Ticket Portal.",
                    from_email="siis-lab-portal@jooust.ac.ke",
                    recipient_list=[obj.student_email],
                    fail_silently=False,
                )
        super().save_model(request, obj, form, change)
