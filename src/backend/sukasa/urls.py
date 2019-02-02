from sukasa.config import API_VERSION

from django.conf.urls import url

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.urlpatterns import format_suffix_patterns

from api.views.reset import ResetDatabase
from api.views.property_data import PropertyDataView, PropertyDataIdView
from api.views.property_valuation import PropertyValuationEstimationView, PropertyValuationDifferentialView


schema_view = get_schema_view(
    openapi.Info(
        title="Sukasa API",
        default_version=API_VERSION,
        description="Sukasa API documentation"
    ),
    validators=['flex', 'ssv'],
    public=True
)

urlpatterns = format_suffix_patterns([
    # Search bulk properties
    url(r'^api/v{}/properties/$'.format(
        API_VERSION),
        PropertyDataView.as_view()),

    # Property by ID
    url(r'^api/v{}/properties/(?P<propertyId>.+)/$'.format(
        API_VERSION),
        PropertyDataIdView.as_view()),

    # Property valuation
    url(r'^api/v{}/property_valuation/estimation/$'.format(
        API_VERSION),
        PropertyValuationEstimationView.as_view()),

    url(r'^api/v{}/property_valuation/differential/$'.format(
        API_VERSION),
        PropertyValuationDifferentialView.as_view()),

    # Reset
    url(r'^api/v{}/reset/all/$'.format(
        API_VERSION),
        ResetDatabase.as_view()),

    # Swagger
    url(r'^api/swagger/$',
        schema_view.with_ui(
            'swagger', cache_timeout=0),
        name='schema-swagger-ui'),

    url(r'^api/redoc/$',
        schema_view.with_ui(
            'redoc', cache_timeout=0),
        name='schema-redoc')
])
