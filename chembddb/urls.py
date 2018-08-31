from django.conf import settings
from django.conf.urls import include, url      #cannot import patterns after Django > 1.80
from django.conf.urls import *
from . import views
# from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

# from django.conf.urls.media import media

app_name = 'chembddb'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'page=(?P<page_no>[0-9]+)/$', views.index, name='index'),
    url(r'submitrequest/$', views.submitRequest, name='submitrequest'),
    url(r'submitrequest/$', views.submitRequest, name='submitrequest'),
    url(r'reviewrequest/$', views.reviewRequest, name='reviewrequest'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_page),
    url(r'^register/success/$', views.register_success),
    url(r'^ID=(?P<mol_graph_id>[0-9]+)/$', views.mol_detail, name='mol_detail'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This is when the debug mode is on for testing purposes

    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
# if settings.DEBUG:
#      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
