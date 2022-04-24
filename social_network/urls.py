from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import home_view


urlpatterns = [
	path('preferences/', include('preferences.urls', namespace='preferences')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('', home_view, name='home-view'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)