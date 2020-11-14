from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from rest_framework.authtoken import views as api_views

from search import views as search_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.SearchView.as_view(), name='search'),

    path('content/', include('blog.apps.content.urls')),

    path('api/', include('blog.apps.api.urls', namespace='api')),
    path('api-token-auth/', api_views.obtain_auth_token, name='api-token-auth'),
] + [
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # .. Existing urls
    url(r'', include('allauth.urls')), # Creates urls like yourwebsite.com/login/
    # url(r'^accounts/', include('allauth.urls')), # Creates urls like yourwebsite.com/accounts/login/


    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
