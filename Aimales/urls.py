from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Aimales.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^aimales/', include('aimales.urls')),
    url(r'^aimales/(?P<enable>(\s\S)+)$', include('aimales.urls')),
)
