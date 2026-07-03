from django.shortcuts import render
from .models import LabTicket

def report_issue(request):
    if request.method == 'POST':
        LabTicket.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            reg_number_or_staff_id=request.POST.get('reg_id'),
            lab_room=request.POST.get('lab_room'),
            computer_number=request.POST.get('comp_num'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
        )
        return render(request, 'lab_portal/report.html', {'success': True})
        
    return render(request, 'lab_portal/report.html')
