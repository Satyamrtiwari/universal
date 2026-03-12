from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.conf import settings
import time
import os

# Important: You will need the 'agora-token-builder' package if you want to generate real tokens
# For now, we will return the room configuration and App ID

class AgoraRoomView(generics.GenericAPIView):
    """
    View to provide Agora configuration for video/audio calls.
    The APP_ID is pulled from the consolidated .env file.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # In a real app, you would use 'RtcTokenBuilder.buildTokenWithUid' here.
        # For the hackathon, we return the App ID and a unique channel name.
        
        channel_name = request.query_params.get('channel', f"consultation-{request.user.id}")
        agora_app_id = os.getenv('AGORA_APP_ID', 'not-configured')
        
        if agora_app_id == 'not-configured':
            return Response({"error": "Agora App ID not found in .env"}, status=400)
            
        return Response({
            "app_id": agora_app_id,
            "channel_name": channel_name,
            "uid": request.user.id,
            "token": "generated-token-placeholder", # To be replaced with real token logic
            "instruction": "Place your Agora App ID in the root .env file"
        })
