from django.contrib import admin
from django.forms.widgets import Media
from django.urls import path, include
from django.conf.urls.static import static
from . import settings  # mediaを使うために

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
   path('admin/', admin.site.urls), 
   path('accounts/', include('accounts.urls')),
   path('myposts/', include('myposts.urls')), 
]
# mediaを使うために追加
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
