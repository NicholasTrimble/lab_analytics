from django.shortcuts import render, redirect
from django.db.models import Count
from .models import QualityTicket, Department, Doctor
from .forms import TicketForm
from google import genai
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def dashboard(request):
    dept_data = Department.objects.annotate(ticket_count=Count('tickets')).values('name', 'ticket_count')
    labels = [item['name'] for item in dept_data]
    counts = [item['ticket_count'] for item in dept_data]

    high_risk_doctors = Doctor.objects.annotate(
        total_remakes=Count('tickets')
    ).filter(total_remakes__gt=0).order_by('-total_remakes')[:3]

    action_plan = []
    
    for doctor in high_risk_doctors:
        top_dept_data = doctor.tickets.values('department__name', 'issue_description').annotate(
            count=Count('id')
        ).order_by('-count').first()

        dept_name = top_dept_data['department__name'] if top_dept_data else "Unknown"
        specific_issue = top_dept_data['issue_description'] if top_dept_data else "Unknown"
        
        if doctor.total_remakes > 10:
            risk_level = "Critical"
        elif doctor.total_remakes > 5:
            risk_level = "High"
        else:
            risk_level = "Medium"

        prompt = f"Act as a dental lab manager. Dr. {doctor.name} has had {doctor.total_remakes} remakes recently. The primary issue is '{specific_issue}' in the {dept_name} department. In exactly two short sentences, give me a professional, actionable retention strategy to save this account and prevent this specific error."

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            ai_suggestion = response.text
        except Exception as e:
            ai_suggestion = "AI suggestion temporarily unavailable."
            print(f"DEBUG ERROR: {e}")

        action_plan.append({
            'name': doctor.name,
            'remakes': doctor.total_remakes,
            'department': f"{dept_name} ({specific_issue})", 
            'risk_level': risk_level,
            'suggestion': ai_suggestion
        })

    context = {
        'labels': labels,
        'counts': counts,
        'action_plan': action_plan,
    }
    
    return render(request, 'tracker/dashboard.html', context)


@login_required(login_url='/admin/login/')
def add_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = TicketForm() 
        
    return render(request, 'tracker/add_ticket.html', {'form': form})