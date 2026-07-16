from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import LabTicket
from .forms import LabTicketForm

# 1. New Clean Homepage Dashboard View
def home_dashboard(request):
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

    recent_resolutions = LabTicket.objects.filter(status='Resolved').order_by('-updated_at')[:5]

    context = {
        'stats': stats,
        'recent_resolutions': recent_resolutions,
    }
    return render(request, 'lab_portal/home.html', context)


# 2. Dedicated Ticket Filing Page View
def report_issue(request):
    active_tickets = LabTicket.objects.filter(status__in=['Pending', 'Assigned'])
    
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
            
            already_flagged = LabTicket.objects.filter(
                lab_room=lab_room, 
                computer_number__iexact=comp_num,
                status__in=['Pending', 'Assigned']
            ).exists()
            
            if already_flagged:
                messages.error(request, f"Error: Computer {comp_num} in {ticket.get_lab_room_display()} already has an active issue reported.")
            else:
                ticket.save()
                messages.success(request, f"Success! Your issue for {comp_num} has been successfully submitted.")
                return redirect('home_dashboard') # Redirect to home page after filing successfully!
    else:
        form = LabTicketForm()

    context = {
        'form': form,
        'flagged_computers': flagged_computers,
    }
    return render(request, 'lab_portal/report.html', context)
