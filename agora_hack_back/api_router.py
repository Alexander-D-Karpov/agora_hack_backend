from django.urls import include, path

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("auth/", include("auth.urls")),
                path("constructor/", include("constructor.urls")),
            ]
        ),
    )
]
