from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import LabTicket

@admin.register(LabTicket)
class LabTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'computer_number', 'category', 'status')
    list_filter = ('status', 'lab_room', 'category')
    search_fields = ('reg_number_or_staff_id', 'computer_number', 'full_name')
    fields = ('status', 'admin_feedback', 'full_name', 'email', 'reg_number_or_staff_id', 'lab_room', 'computer_number', 'category', 'description')

    def save_model(self, request, obj, form, change):
        # Check if the ticket is being updated to Resolved
        if change and obj.status == 'Resolved':
            subject = f"RESOLVED: SIIS Lab Issue - Ticket #{obj.id}"
            message = f"Hello {obj.full_name},\n\nThe issue you reported regarding {obj.computer_number} ({obj.category}) at JOOUST SIIS Labs has been successfully resolved.\n\nAdmin Feedback:\n{obj.admin_feedback or 'No specific notes provided.'}\n\nThank you,\nSIIS Lab Administration\nJaramogi Oginga Odinga University of Science and Technology."
            
            # Send email notifications out
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [obj.email],
                fail_silently=True,
            )
        super().save_model(request, obj, form, change)
