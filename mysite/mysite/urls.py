from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from .api import api_router


# 不需要 i18n 的 URL 模式
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("api/", include("api.urls")),
    path("api/v2/", api_router.urls),
]

# 需要 i18n 的 URL 模式
urlpatterns += i18n_patterns(
    path("search/", search_views.search, name="search"),
    re_path(r"", include(wagtail_urls)),
    prefix_default_language=True,
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 移除了重复的 Wagtail URLs，因为它们已经包含在 i18n_patterns 中
