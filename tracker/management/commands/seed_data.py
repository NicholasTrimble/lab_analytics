from django.core.management.base import BaseCommand
from tracker.models import Doctor, Department, QualityTicket
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with synthetic lab QA data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        QualityTicket.objects.all().delete()
        Doctor.objects.all().delete()
        Department.objects.all().delete()

        depts = {
            "Setup": ["Midline off", "Improper overjet/overbite"],
            "Baseplate": ["Loose fit on model", "Overextended borders"],
            "Model Room": ["Bubbles in prep", "Mounted off bite"],
            "Crown & Bridge": ["Short margin", "Open contact", "High occlusion"],
            "Ceramics": ["Wrong shade", "Porosity in porcelain"]
        }
        
        dept_objects = {}
        for d_name in depts.keys():
            dept, _ = Department.objects.get_or_create(name=d_name)
            dept_objects[d_name] = dept

        doctors = [Doctor.objects.create(name=f"Dr. {fake.last_name()}") for _ in range(20)]

        statuses = ['Resolved', 'Remake in Progress', 'Credited']
        for _ in range(300):
            doc = random.choice(doctors)
            dept_name = random.choice(list(depts.keys()))
            dept_obj = dept_objects[dept_name]
            issue = random.choice(depts[dept_name])
            
            status = random.choices(statuses, weights=[70, 20, 10])[0]

            QualityTicket.objects.create(
                doctor=doc,
                department=dept_obj,
                issue_description=issue,
                status=status
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 300 QA tickets!'))