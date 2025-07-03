from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        return Response({
            'success': True,
            'message': 'Register successfully',
            'data': 'Ok!',
        }, status=status.HTTP_201_CREATED)
