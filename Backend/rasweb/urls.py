from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from Apps.User import urls as user_urls
from Apps.Chat import urls as chat_urls
from Apps.Post import urls as post_urls
from Apps.LiveStream import urls as live_urls
from Apps.Inventory import urls as inventory_urls

url_base = 'robotarium-api/v1.0/'

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # User app apis
                  path(url_base, include(user_urls)),

                  # Post app apis
                  path(url_base, include(post_urls)),

                  # Chat app apis
                  path(url_base, include(chat_urls)),

                  # LiveStream app apis
                  path(url_base, include(live_urls)),

                  # Inventory app apis
                  path(url_base, include(inventory_urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
