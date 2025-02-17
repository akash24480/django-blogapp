from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.create_blog, name="create_blog"),
    path("update_blog/<int:blog_id>/", views.update_blog, name="update_blog"),
    path("delete_blog/<int:blog_id>/", views.delete_blog, name="delete_blog")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)