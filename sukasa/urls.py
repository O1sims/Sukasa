import config

from django.conf.urls import url

from api.views.index import IndexView
from api.views.reset import ResetView, ResetIndexView
from api.views.property_data import GeneratePropertyDataView, PropertyDataView, PropertyIdView

from rest_framework.urlpatterns import format_suffix_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Sukasa API",
        default_version=config.API_VERSION,
        description="Sukasa API documentation"
    ),
    validators=['flex', 'ssv'],
    public=True
)

urlpatterns = format_suffix_patterns([
    # Bulk properties
    url(r'^api/v{}/properties/(?P<property_type>.+)/$'.format(
        config.API_VERSION),
        PropertyDataView.as_view()),

    # Property by ID
    url(r'^api/v{}/property/(?P<property_type>.+)/(?P<property_id>.+)/$'.format(
        config.API_VERSION),
        PropertyIdView.as_view()),

    # Generate property data
    url(r'^api/v{}/generate_dataset/$'.format(
        config.API_VERSION),
        GeneratePropertyDataView.as_view()),

    # Reset
    url(r'^api/v{}/reset/all/$'.format(
        config.API_VERSION),
        ResetView.as_view()),

    url(r'^api/v{}/reset/index/(?P<index>.+)/$'.format(
        config.API_VERSION),
        ResetIndexView.as_view()),

    # Swagger
    url(r'^swagger/$',
        schema_view.with_ui(
            'swagger', cache_timeout=0),
        name='schema-swagger-ui'),

    url(r'^redoc/$',
        schema_view.with_ui(
            'redoc', cache_timeout=0),
        name='schema-redoc'),

    # Angular
    url(r'^$',
        IndexView.as_view()),

    url(r'^(?P<path>.*)/$',
        IndexView.as_view())
])
