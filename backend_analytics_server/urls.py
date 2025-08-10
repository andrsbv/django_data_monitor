from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # home del dashboard (protegido con @login_required en la vista)
    path('', include('dashboard.urls')),

    # auth
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='security/login.html',
            redirect_authenticated_user=False
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/login/'),
        name='logout'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
