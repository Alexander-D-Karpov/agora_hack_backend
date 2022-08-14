from rest_framework import generics
from rest_framework.parsers import FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from constructor.api.serializers import FontFamilySerializer
from constructor.models import FontFamily


class ListCreateFontsApiView(generics.ListCreateAPIView):
    serializer_class = FontFamilySerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FontFamily.objects.first(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
