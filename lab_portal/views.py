from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import LabTicket
from .forms import LabTicketForm

def report_issue(request):
    if request.method == 'POST':
        form = LabTicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your issue has been successfully submitted to the SIIS Lab Admin!")
            return redirect('report_issue')
    else:
        form = LabTicketForm()

    # --- 1. Calculate Live Lab Status Badges ---
    TOTAL_COMPUTERS = 40
    
    labs_data = LabTicket.objects.values('lab_room').annotate(
        pending_count=Count('id', filter=Q(status__in=['Pending', 'Assigned']))
    )
    
    stats = {
        'LAB_1': {'active_issues': 0, 'health': 100, 'color': 'emerald'},
        'SIIS_LAB': {'active_issues': 0, 'health': 100, 'color': 'emerald'},
        'MULTIDISCIPLINARY': {'active_issues': 0, 'health': 100, 'color': 'emerald'},
    }
    
    for l in labs_data:
        room = l['lab_room']
        active = l['pending_count']
        if room in stats:
            stats[room]['active_issues'] = active
            health = max(0, int(((TOTAL_COMPUTERS - active) / TOTAL_COMPUTERS) * 100))
            stats[room]['health'] = health
            if health < 80:
                stats[room]['color'] = 'red'
            elif health < 95:
                stats[room]['color'] = 'amber'

    # --- 2. Fetch Recent Resolutions Feed ---
    recent_resolutions = LabTicket.objects.filter(status='Resolved').order_by('-updated_at')[:4]

    context = {
        'form': form,
        'stats': stats,
        'recent_resolutions': recent_resolutions,
    }
    return render(request, 'lab_portal/report.html', context)
