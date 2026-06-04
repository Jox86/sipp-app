from django.urls import path, include

urlpatterns = [
    path('', include('api.v1.urls.user_urls')),
    path('', include('api.v1.urls.project_urls')),
    path('', include('api.v1.urls.report_urls')),
    path('', include('api.v1.urls.dashboard_urls')),
    path('', include('api.v1.urls.help_urls')),
]
