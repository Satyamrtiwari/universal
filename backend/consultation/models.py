from django.db import models
from django.conf import settings

class ConsultationRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations_as_patient')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations_as_doctor')
    specialty_required = models.CharField(max_length=100)
    ai_summary = models.TextField(null=True, blank=True)
    urgency_level = models.CharField(max_length=10, choices=(('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')), default='LOW')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Consultation {self.id} - {self.patient.username}"

class Prescription(models.Model):
    consultation = models.OneToOneField(ConsultationRequest, on_delete=models.CASCADE, related_name='prescription')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription_text = models.TextField()
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.consultation.patient.username}"
