from django.urls import path
from .views import ArtWorkListView, upload_artwork, ArtWorkDetailView
from django.conf import settings
from django.conf.urls.static import static
from .consumers import ArtWorkConsumer

urlpatterns = [
    path('', ArtWorkListView.as_view(), name='home'),
    
    path('upload/', upload_artwork, name='upload_artwork'),

    path('artwork/<int:artwork_id>/', ArtWorkDetailView.as_view(), name='artwork_detail'),

    path('ws/artwork/<int:artwork_id>/', ArtWorkConsumer.as_asgi()),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)