import config

from django.conf.urls import url

from api.views.index import IndexView
from api.views.reset import ResetIndexView
from api.views.property_data import GeneratePropertyDataView, GetPropertyDataView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view


urlpatterns = format_suffix_patterns([
    url(r'^api/v{}/properties/(?P<property_type>.+)/$'.format(
        config.API_VERSION),
        GetPropertyDataView.as_view()),

    url(r'^api/v{}/generate_dataset/$'.format(
        config.API_VERSION),
        GeneratePropertyDataView.as_view()),

    url(r'^api/v{}/reset/(?P<index>.+)/$'.format(
        config.API_VERSION),
        ResetIndexView.as_view()),

    url(r'^swagger/$',
        get_swagger_view(
            title='Sukasa API')),

    url(r'^$',
        IndexView.as_view(),
        name='index')
])
