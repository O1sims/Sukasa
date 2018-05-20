from django.conf.urls import url

from api.views.index import IndexView
from api.views.property_data import CollectPropertyDataView, GetPropertyDataView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view


urlpatterns = format_suffix_patterns([
    url(r'^application/properties/(?P<property_type>.+)/$',
        GetPropertyDataView.as_view()),

    url(r'^application/collect_properties/$',
        CollectPropertyDataView.as_view()),

    url(r'^swagger/$',
        get_swagger_view(
            title='Sukasa API')),

    url(r'^$',
        IndexView.as_view(),
        name='index')
])
