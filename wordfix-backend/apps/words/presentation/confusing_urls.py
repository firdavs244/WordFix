"""
Confusing pairs URL routing.
"""

from django.urls import path

from .views import (
    ConfusingPairCountView,
    ConfusingPairDetailView,
    ConfusingPairDrillView,
    ConfusingPairResolveView,
    ConfusingPairsListView,
)

app_name = "confusing-pairs"

urlpatterns = [
    path("", ConfusingPairsListView.as_view(), name="confusing-pairs-list"),
    path("count/", ConfusingPairCountView.as_view(), name="confusing-pairs-count"),
    path("<uuid:pair_id>/", ConfusingPairDetailView.as_view(), name="confusing-pair-detail"),
    path("<uuid:pair_id>/drill/", ConfusingPairDrillView.as_view(), name="confusing-pair-drill"),
    path("<uuid:pair_id>/resolve/", ConfusingPairResolveView.as_view(), name="confusing-pair-resolve"),
]
