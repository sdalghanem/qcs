"""
URL configuration for qcs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
#from clients.admin import custom_admin_site
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('myadmin/', custom_admin_site.urls),

    path('cloudteam/', include('cloudteam.urls')),
    path('clients/', include('clients.urls')),
    path('preset/', include('preset.urls')),
    path('report/', include('report.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # صفحة تأكيد إرسال البريد
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # رابط تعيين كلمة المرور الجديد
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # صفحة نجاح إعادة التعيين
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
