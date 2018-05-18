"""casa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
