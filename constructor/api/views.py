from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import AuthenticationFailed

from constructor.api.serializers import (
    FontFamilySerializer,
    FullTextBlockSerializer,
    SiteSerializer,
    ImageBlockSerializer,
    SliderBlockSerializer,
    SlideImageSerializer,
    IframeBlockSerializer,
    RowBlockSerializer,
    ColumnBlockSerializer,
    FormBlockSerializer,
    FormFieldSerializer,
)
from constructor.models import FontFamily, Site, Form, FormField
from constructor.services.forms import submit_form
from constructor.services.site_map import get_site_map


class ListCreateSiteApiView(generics.ListCreateAPIView):
    serializer_class = SiteSerializer

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)


class ListCreateFontsApiView(generics.ListCreateAPIView):
    serializer_class = FontFamilySerializer

    def get_queryset(self):
        return FontFamily.objects.filter(user=self.request.user)


class CreateTextBlockApiView(generics.CreateAPIView):
    serializer_class = FullTextBlockSerializer


class CreateImageBlockApiView(generics.CreateAPIView):
    serializer_class = ImageBlockSerializer
    parser_classes = (MultiPartParser,)


class AddSlideImageApiView(generics.CreateAPIView):
    serializer_class = SlideImageSerializer
    parser_classes = (MultiPartParser,)


class CreateSlideBlockApiView(generics.CreateAPIView):
    serializer_class = SliderBlockSerializer


class CreateIframeBlockApiView(generics.CreateAPIView):
    serializer_class = IframeBlockSerializer


class CreateRowApiView(generics.CreateAPIView):
    serializer_class = RowBlockSerializer


class CreateColumnApiView(generics.CreateAPIView):
    serializer_class = ColumnBlockSerializer


class CreateFormApiView(generics.CreateAPIView):
    serializer_class = FormBlockSerializer


class ListCreateFormFieldApiView(generics.ListCreateAPIView):
    serializer_class = FormFieldSerializer

    def get_queryset(self):
        form = get_object_or_404(
            Form, slug=self.request.parser_context["kwargs"]["form_slug"]
        )
        if form.site.user != self.request.user:
            raise AuthenticationFailed
        return form.fields.all()

    @swagger_auto_schema(operation_id="list_form_fields")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="create_form_field")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetUpdateDeleteFormFieldApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FormFieldSerializer

    def get_object(self):
        form_field = get_object_or_404(
            FormField, id=self.request.parser_context["kwargs"]["field_id"]
        )
        if form_field.form.site.user != self.request.user:
            raise AuthenticationFailed
        return form_field


class SubmitFormApiView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = []
    authentication_classes = []

    def post(self, request, form_slug):
        form = get_object_or_404(Form, slug=form_slug)
        submit_form(request.data, form)
        return Response(status=status.HTTP_201_CREATED)


class ListSiteBlocks(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, slug):
        return Response(get_site_map(slug))
