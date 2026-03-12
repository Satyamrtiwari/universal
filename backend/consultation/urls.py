from django.urls import path
from .views_agora import AgoraRoomView
from .views_records import PatientHealthRecordView
from .views import RequestConsultationView, ConsultationListView, PrescriptionCreateView

urlpatterns = [
    path('request/', RequestConsultationView.as_view(), name='request-consultation'),
    path('list/', ConsultationListView.as_view(), name='consultation-list'),
    path('agora-config/', AgoraRoomView.as_view(), name='agora-config'),
    path('health-passport/', PatientHealthRecordView.as_view(), name='health-passport'),
    path('prescribe/', PrescriptionCreateView.as_view(), name='prescribe'),
]
