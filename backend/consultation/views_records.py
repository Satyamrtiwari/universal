from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ConsultationRequest, Prescription
from .serializers import ConsultationRequestSerializer, PrescriptionSerializer

class PatientHealthRecordView(generics.GenericAPIView):
    """
    View for patients to see their own medical history (Digital Health Passport).
    Strictly follows 'GenericAPIView' and filters for the logged-in user.
    """
    serializer_class = ConsultationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Only show completed consultations with prescriptions for the record
        queryset = ConsultationRequest.objects.filter(
            patient=request.user, 
            status='COMPLETED'
        ).order_by('-created_at')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "patient_name": f"{request.user.first_name} {request.user.last_name}",
            "records_count": queryset.count(),
            "history": serializer.data
        })
