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
<<<<<<< HEAD
    url(r'^nlp_tag_tools.html$', views.nlpTagTools),
=======
>>>>>>> 82c87a3c131a95bcda66203a7f21262c5609a8bf
)
