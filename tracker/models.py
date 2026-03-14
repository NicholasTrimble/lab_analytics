from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class QualityTicket(models.Model):
    STATUS_CHOICES = [
        ('Resolved', 'Resolved'),
        ('Remake in Progress', 'Remake in Progress'),
        ('Credited', 'Credited'),
    ]
    
    date_logged = models.DateField(auto_now_add=True) 
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='tickets')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='tickets')
    
    issue_description = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Resolved')

    def __str__(self):
        return f"{self.date_logged} | {self.doctor.name} | {self.department.name}"