from django.conf.urls import include, url
from django.contrib import admin
import app

urlpatterns = [
    # Examples:
    # url(r'^$', 'wikibooks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
