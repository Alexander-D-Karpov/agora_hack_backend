from django.urls import path

from constructor.api.views import (
    ListCreateFontsApiView,
    CreateTextBlockApiView,
    ListCreateSiteApiView,
    CreateImageBlockApiView,
    CreateSlideBlockApiView,
    AddSlideImageApiView,
    CreateIframeBlockApiView,
    CreateRowApiView,
    CreateColumnApiView,
    ListSiteBlocks,
    CreateFormApiView,
    ListCreateFormFieldApiView,
    GetUpdateDeleteFormFieldApiView,
    SubmitFormApiView,
)

urlpatterns = [
    path("site/", ListCreateSiteApiView.as_view(), name="list_create_site_api"),
    path("site/<str:slug>", ListSiteBlocks.as_view(), name="list_site_api"),
    path("site/form/<form_slug>", SubmitFormApiView.as_view(), name="submit_form_api"),
    # path("site/form/field/<int:field_id>", AnswerFormFieldApiView.as_view(), name="answer_field_api"),
    path("fonts/", ListCreateFontsApiView.as_view(), name="list_create_font_api"),
    path(
        "<str:site_name>/blocks/text/",
        CreateTextBlockApiView.as_view(),
        name="create_text_api",
    ),
    path(
        "<str:site_name>/blocks/image/",
        CreateImageBlockApiView.as_view(),
        name="create_image_api",
    ),
    path(
        "<str:site_name>/blocks/slide/",
        CreateSlideBlockApiView.as_view(),
        name="create_slide_api",
    ),
    path(
        "<str:site_name>/blocks/slide/image/",
        AddSlideImageApiView.as_view(),
        name="add_slide_image_api",
    ),
    path(
        "<str:site_name>/blocks/iframe/",
        CreateIframeBlockApiView.as_view(),
        name="create_iframe_api",
    ),
    path(
        "<str:site_name>/blocks/row/",
        CreateRowApiView.as_view(),
        name="create_row_api",
    ),
    path(
        "<str:site_name>/blocks/column/",
        CreateColumnApiView.as_view(),
        name="create_column_api",
    ),
    path(
        "<str:site_name>/blocks/form/",
        CreateFormApiView.as_view(),
        name="create_form_api",
    ),
    path(
        "<str:site_name>/blocks/form/<str:form_slug>",
        ListCreateFormFieldApiView.as_view(),
        name="create_form_api",
    ),
    path(
        "<str:site_name>/blocks/form/<str:form_slug>/<int:field_id>",
        GetUpdateDeleteFormFieldApiView.as_view(),
        name="get_update_delete_api",
    ),
]
