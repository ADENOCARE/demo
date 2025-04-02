from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from classifier.views import (
    classify_image, 
    index,
    register, 
    symptom_checker, 
    community, 
    home, 
    share_story,
    account_view,
    logout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('symptom-checker/', symptom_checker, name='symptom_checker'),  # Hyphen recommended for URLs
    path('community/', community, name='community'),
    path('share-story/', share_story, name='share_story'),  # Hyphen recommended
    path('classify/', classify_image, name='upload_image'),  # Changed from 'classifier/'
    path('account/', account_view, name='account'),
    path('logout/', logout_view, name='logout'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)