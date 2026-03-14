from django.shortcuts import render, redirect
from django.db.models import Count
from .models import QualityTicket, Department, Doctor
from .forms import TicketForm

def dashboard(request):
    dept_data = Department.objects.annotate(ticket_count=Count('tickets')).values('name', 'ticket_count')
    labels = [item['name'] for item in dept_data]
    counts = [item['ticket_count'] for item in dept_data]

    high_risk_doctors = Doctor.objects.annotate(
        total_remakes=Count('tickets')
    ).filter(total_remakes__gt=0).order_by('-total_remakes')[:6]

    action_plan = []
    
    for doctor in high_risk_doctors:
        top_dept = doctor.tickets.values('department__name').annotate(
            count=Count('id')
        ).order_by('-count').first()

        dept_name = top_dept['department__name'] if top_dept else "Unknown"
        
        if dept_name == "Crown & Bridge":
            suggestion = "High churn risk. Route next 5 cases to a Senior Tech and call clinic to verify margin preferences."
            risk_level = "Critical"
        elif dept_name == "Setup" or dept_name == "Baseplate":
            suggestion = "Aesthetic/Fit issues detected. Schedule a quick sync with the doctor to review midline and overjet expectations."
            risk_level = "High"
        elif dept_name == "Model Room":
            suggestion = "Internal lab error. Retrain model room staff on this doctor's specific impression material to prevent distortion."
            risk_level = "Medium"
        else:
            suggestion = "Monitor closely. Send a 'Thank You' note with their next completed case to rebuild goodwill."
            risk_level = "Medium"

        action_plan.append({
            'name': doctor.name,
            'remakes': doctor.total_remakes,
            'department': dept_name,
            'risk_level': risk_level,
            'suggestion': suggestion
        })

    context = {
        'labels': labels,
        'counts': counts,
        'action_plan': action_plan,
    }
    
    return render(request, 'tracker/dashboard.html', context)



def add_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = TicketForm() 
        
    return render(request, 'tracker/add_ticket.html', {'form': form})