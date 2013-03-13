from django.conf.urls import patterns, include, url

from DUlSine import urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^DUlSine/', include('DUlSine.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
