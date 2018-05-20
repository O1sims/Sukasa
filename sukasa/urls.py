from django.conf.urls import url

from api.views.index import IndexView
from api.views.collect_property_data import CollectPropertyDataView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view


urlpatterns = format_suffix_patterns([
    url(r'^swagger/$',
        get_swagger_view(
            title='Sukasa API')),

    url(r'^application/collect_property_data/$',
        CollectPropertyDataView.as_view()),

    url(r'^$',
        IndexView.as_view(),
        name='index')
])
