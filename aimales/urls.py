from django.conf.urls import patterns, include, url

from django.contrib import admin
from aimales import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Aimales.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', views.loginIndex),
    url(r'^login$', views.loginIndex),
    url(r'^index.html$', views.aimalesIndex),
    url(r'^loginValidate$', views.loginValidate),
    url(r'^nlp_tag_tools.html$', views.nlpTagTools),
    url(r'^datasets/(?P<dataset>\S+)/(?P<flag>\S+)/(?P<flag_value>\S+)$', views.fetchDataset),
)
