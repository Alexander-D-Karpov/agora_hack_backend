from django.urls import path

from constructor.api.views import (
    ListCreateFontsApiView,
    CreateTextBlockApiView,
    ListCreateSiteApiView,
    CreateImageBlockApiView,
    CreateSlideBlockApiView,
    AddSlideImageApiView,
    CreateIframeBlockApiView,
    CreateRowSerializer,
    CreateColumnSerializer, ListSiteBlocks,
)

urlpatterns = [
    path("site/", ListCreateSiteApiView.as_view(), name="list_create_site_api"),
    path("site/<str:slug>", ListSiteBlocks.as_view(), name="list_site_api"),
    path("fonts/", ListCreateFontsApiView.as_view(), name="list_create_font_api"),
    path(
        "<str:slug>/blocks/text/",
        CreateTextBlockApiView.as_view(),
        name="create_text_api",
    ),
    path(
        "<str:slug>/blocks/image/",
        CreateImageBlockApiView.as_view(),
        name="create_image_api",
    ),
    path(
        "<str:slug>/blocks/slide/",
        CreateSlideBlockApiView.as_view(),
        name="create_slide_api",
    ),
    path(
        "<str:slug>/blocks/slide/image/",
        AddSlideImageApiView.as_view(),
        name="add_slide_image_api",
    ),
    path(
        "<str:slug>/blocks/iframe/",
        CreateIframeBlockApiView.as_view(),
        name="create_iframe_api",
    ),
    path(
        "<str:slug>/blocks/row/",
        CreateRowSerializer.as_view(),
        name="create_row_api",
    ),
    path(
        "<str:slug>/blocks/column/",
        CreateColumnSerializer.as_view(),
        name="create_column_api",
    ),
]
