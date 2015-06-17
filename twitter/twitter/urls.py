from django.conf.urls import patterns, include, url
from stream_manager.views import LiveStream
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='index.html')),
                       url(r'^live-stream', LiveStream.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       )
