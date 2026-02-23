"""
Word URL routing.
"""

from django.urls import path

from .views import (
    AnalyzeTextView,
    CSVImportView,
    CSVValidateView,
    EnrichAllView,
    EnrichmentRetryView,
    EnrichmentStatusView,
    EnrichWordView,
    ImportAddWordsView,
    WordBulkCreateView,
    WordCategoryDeleteView,
    WordCategoryListCreateView,
    WordDetailView,
    WordListCreateView,
    WordReviewView,
    WordStatsView,
)
from .views.archive_views import (
    ArchiveWordView,
    ArchivedWordsListView,
    BulkArchiveView,
    UnarchiveWordView,
)

app_name = "words"

urlpatterns = [
    path("", WordListCreateView.as_view(), name="word-list-create"),
    path("bulk/", WordBulkCreateView.as_view(), name="word-bulk-create"),
    path("stats/", WordStatsView.as_view(), name="word-stats"),
    path("review/", WordReviewView.as_view(), name="word-review"),
    path("enrich-all/", EnrichAllView.as_view(), name="enrich-all"),
    path("import/analyze/", AnalyzeTextView.as_view(), name="import-analyze"),
    path("import/add/", ImportAddWordsView.as_view(), name="import-add"),
    path("import/csv/validate/", CSVValidateView.as_view(), name="csv-validate"),
    path("import/csv/", CSVImportView.as_view(), name="csv-import"),
    path("archived/", ArchivedWordsListView.as_view(), name="archived-list"),
    path("archive/bulk/", BulkArchiveView.as_view(), name="bulk-archive"),
    path("<uuid:word_id>/", WordDetailView.as_view(), name="word-detail"),
    path("<uuid:word_id>/enrich/", EnrichWordView.as_view(), name="word-enrich"),
    path("<uuid:word_id>/enrichment-status/", EnrichmentStatusView.as_view(), name="word-enrichment-status"),
    path("<uuid:word_id>/enrichment-retry/", EnrichmentRetryView.as_view(), name="word-enrichment-retry"),
    path("<uuid:word_id>/archive/", ArchiveWordView.as_view(), name="word-archive"),
    path("<uuid:word_id>/unarchive/", UnarchiveWordView.as_view(), name="word-unarchive"),
    path("categories/", WordCategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<uuid:category_id>/", WordCategoryDeleteView.as_view(), name="category-delete"),
]
