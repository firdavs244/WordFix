"""
WordFix URL Configuration.

API versioning: all endpoints under /api/v1/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/", include("apps.users.presentation.urls")),
    path("api/v1/auth/onboarding/", include("apps.users.presentation.onboarding_urls")),
    path("api/v1/words/", include("apps.words.presentation.urls")),
    path("api/v1/words/confusing-pairs/", include("apps.words.presentation.confusing_urls")),
    path("api/v1/review/", include("apps.words.presentation.review_urls")),
    path("api/v1/tests/", include("apps.words.presentation.testing_urls")),
    path("api/v1/games/", include("apps.words.presentation.game_urls")),
    path("api/v1/chat/", include("apps.words.presentation.chat_urls")),
    path("api/v1/analytics/", include("apps.words.presentation.analytics_urls")),
    path("api/v1/challenges/", include("apps.words.presentation.challenge_urls")),
    path("api/v1/notifications/", include("apps.users.presentation.notification_urls")),
    path("api/v1/immersive/", include("apps.immersive.presentation.urls")),
    path("api/v1/system/", include("apps.common.urls")),
    path("api/v1/learning-profile/", include("apps.users.presentation.learning_urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
