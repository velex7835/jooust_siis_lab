from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LabTicketForm

def report_issue(request):
    if request.method == 'POST':
        # Added request.FILES to capture uploaded screenshots
        form = LabTicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your issue has been successfully submitted to the SIIS Lab Admin!")
            return redirect('report_issue')
    else:
        form = LabTicketForm()
        
    return render(request, 'lab_portal/report.html', {'form': form})
