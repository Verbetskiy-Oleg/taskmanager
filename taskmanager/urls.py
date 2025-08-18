from django.contrib import admin
from django.urls import path, include
from tasks import views as task_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", task_views.register, name="register"),
    path("", include("tasks.urls")),
    path("", include("django.contrib.auth.urls")),
]
