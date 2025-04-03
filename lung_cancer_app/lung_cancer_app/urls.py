from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from classifier.views import (
    classify_image, 
    index,
    register, 
    voice_chatbot, 
    community, 
    home, 
    share_story,
    account_view,
    logout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('voice-chatbot/', voice_chatbot, name='voice_chatbot'),  
    path('community/', community, name='community'),
    path('share-story/', share_story, name='share_story'),  
    path('classify/', classify_image, name='upload_image'), 
    path('account/', account_view, name='account'),
    path('logout/', logout_view, name='logout'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)