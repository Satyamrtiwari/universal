from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ConsultationRequest, Prescription
from .serializers import ConsultationRequestSerializer, PrescriptionSerializer
import uuid

class RequestConsultationView(generics.GenericAPIView):
    serializer_class = ConsultationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Generate a unique room name for the consultation
            room_name = f"telehealth-{uuid.uuid4().hex[:8]}"
            
            serializer.save(
                patient=request.user,
                room_name=room_name,
                status='PENDING'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultationListView(generics.GenericAPIView):
    serializer_class = ConsultationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        if request.user.role == 'DOCTOR':
            queryset = ConsultationRequest.objects.filter(status='PENDING')
        else:
            queryset = ConsultationRequest.objects.filter(patient=request.user)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class PrescriptionCreateView(generics.GenericAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if request.user.role != 'DOCTOR':
            return Response({"error": "Only doctors can provide prescriptions"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            consultation_id = request.data.get('consultation')
            try:
                consultation = ConsultationRequest.objects.get(id=consultation_id)
                # Ensure the consultation is assigned to this doctor or is available
                consultation.status = 'COMPLETED'
                consultation.doctor = request.user
                consultation.save()
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ConsultationRequest.DoesNotExist:
                return Response({"error": "Consultation not found"}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
