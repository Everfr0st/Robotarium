from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from Apps.User import urls as user_urls
from Apps.Chat import urls as chat_urls

url_base = 'coco-api/v1.0/'

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # User models
                  path(url_base, include(user_urls)),

                  #Chat models
                  path(url_base, include(chat_urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
