
from django.urls import path
from .views import BlogView, PublicBlogVIew

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('blog/', BlogView.as_view()),
    path('',PublicBlogVIew.as_view()),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)