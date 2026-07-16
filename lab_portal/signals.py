from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import LabTicket

@receiver(post_save, sender=LabTicket)
def send_resolution_email(sender, instance, created, **kwargs):
    # Only trigger when the ticket is updated to 'Resolved' and student email was provided
    if not created and instance.status == 'Resolved' and instance.student_email:
        subject = f"🛠️ Issue Resolved: Terminal {instance.computer_number} in {instance.get_lab_room_display()}"
        message = (
            f"Dear Student,\n\n"
            f"We are happy to inform you that the issue you reported concerning "
            f"Terminal {instance.computer_number} in the {instance.get_lab_room_display()} "
            f"has been successfully resolved by our IT Operations Team!\n\n"
            f"Details:\n"
            f"- Category: {instance.get_category_display()}\n"
            f"- Issue Description: {instance.description}\n\n"
            f"Thank you for helping us keep the JOOUST SIIS Computer Labs running smoothly.\n\n"
            f"Best Regards,\n"
            f"JOOUST SIIS Lab Operations Team"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.student_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to {instance.student_email}: {e}")
