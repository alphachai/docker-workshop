from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import path

urlpatterns = [
    path('__health/', include('health_check.urls')),
    path('admin/', admin.site.urls),
    path('', include('scorekeeper.urls', namespace='scorekeeper')),
]

if settings.DEBUG:
    # Add view for Django settings
    from config import debug
    urlpatterns += [
        path('_debug_info/', debug.splode),
    ]

    # Add views to debug error templates
    import django.views.defaults
    urlpatterns += [
        path('_debug_404/', django.views.defaults.page_not_found),
        path('_debug_500/', django.views.defaults.server_error),
        path('_debug_400/', django.views.defaults.bad_request),
        path('_debug_403/', django.views.defaults.permission_denied),
    ]

    # Add static files URL
    import django.contrib.staticfiles.urls
    urlpatterns += django.contrib.staticfiles.urls.urlpatterns
