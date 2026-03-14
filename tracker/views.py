from django.shortcuts import render
from django.db.models import Count
from .models import QualityTicket, Department

def dashboard(request):
    dept_data = Department.objects.annotate(ticket_count=Count('tickets')).values('name', 'ticket_count')
    
    labels = [item['name'] for item in dept_data]
    counts = [item['ticket_count'] for item in dept_data]

    context = {
        'labels': labels,
        'counts': counts,
    }
    
    return render(request, 'tracker/dashboard.html', context)