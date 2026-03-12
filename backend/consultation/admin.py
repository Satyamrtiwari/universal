from django.contrib import admin
from .models import ConsultationRequest, Prescription

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'specialty_required', 'status', 'urgency_level', 'created_at')
    list_filter = ('status', 'urgency_level', 'specialty_required')
    search_fields = ('patient__username', 'doctor__username', 'room_name')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'created_at')
    search_fields = ('consultation__patient__username', 'diagnosis')
