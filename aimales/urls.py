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
    url(r'^nlp_tools/record_overview.html$', views.recordOverview),
    url(r'^nlp_tools/nlp_tag_tools.html$', views.nlpTagTools),
    url(r'^nlp_tools/nlp_relation_tools.html$', views.nlpRelationTools),
    url(r'^nlp_tools/nlp_segmentation_tools.html$', views.nlpSegmentationTools),
    url(r'^datasets/(?P<dataset>\S+)/(?P<flag>\S+)/(?P<flag_value>\S+)$', views.fetchDataset),
    url(r'^edit_dataset/(?P<dataset>\S+)/(?P<operation>\S+)/(?P<record_id>\d+)$', views.editDataset),
    url(r'^ner_manual_tag/(?P<dataset>\S+)/edit_tags/(?P<record_id>\S+)$', views.editRecords),
)
