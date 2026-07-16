from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings
from .models import LabTicket
from .forms import LabTicketForm

def report_issue(request):
    # Fetch list of active issues (Pending/Assigned) to flag occupied computers
    active_tickets = LabTicket.objects.filter(status__in=['Pending', 'Assigned'])
    
    # Create a mapping of flagged computers: e.g., {'LAB_1': ['COMP-04', 'COMP-12'], 'SIIS_LAB': ['COMP-01']}
    flagged_computers = {}
    for ticket in active_tickets:
        room = ticket.lab_room
        if room not in flagged_computers:
            flagged_computers[room] = []
        flagged_computers[room].append(ticket.computer_number.upper().strip())

    if request.method == 'POST':
        form = LabTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            lab_room = ticket.lab_room
            comp_num = ticket.computer_number.upper().strip()
            
            # Backend Guard: double check if this computer is already flagged
            already_flaged = LabTicket.objects.filter(
                lab_room=lab_room, 
                computer_number__iexact=comp_num,
                status__in=['Pending', 'Assigned']
            ).exists()
            
            if already_flaged:
                messages.error(request, f"Error: Computer {comp_num} in {ticket.get_lab_room_display()} already has an active issue reported.")
            else:
                ticket.save()
                messages.success(request, f"Your issue for {comp_num} has been successfully submitted!")
                return redirect('report_issue')
    else:
        form = LabTicketForm()

    # --- Calculate Dynamic Lab Status Badges ---
    # Real Capacities
    capacities = {
        'LAB_1': 20,
        'SIIS_LAB': 28,
        'MULTIDISCIPLINARY': 80
    }
    
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
            total_seats = capacities.get(room, 40)
            stats[room]['active_issues'] = active
            health = max(0, int(((total_seats - active) / total_seats) * 100))
            stats[room]['health'] = health
            if health < 80:
                stats[room]['color'] = 'red'
            elif health < 95:
                stats[room]['color'] = 'amber'

    # Fetch Recent Resolutions Feed
    recent_resolutions = LabTicket.objects.filter(status='Resolved').order_by('-updated_at')[:4]

    context = {
        'form': form,
        'stats': stats,
        'recent_resolutions': recent_resolutions,
        'flagged_computers': flagged_computers,  # Sent to JS frontend for dynamic map lockout
    }
    return render(request, 'lab_portal/report.html', context)
