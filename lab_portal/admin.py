from django.contrib import admin
from .models import LabTicket

@admin.register(LabTicket)
class LabTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'reported_by', 'lab_room', 'computer_number', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'lab_room', 'reported_by')
    search_fields = ('computer_number', 'description')
