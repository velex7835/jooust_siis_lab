from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LabTicketForm

def report_issue(request):
    if request.method == 'POST':
        form = LabTicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your issue has been successfully submitted!")
            return redirect('/admin/')  # Redirects straight to the Admin channel login/dashboard
    else:
        form = LabTicketForm()
        
    return render(request, 'lab_portal/report.html', {'form': form})
