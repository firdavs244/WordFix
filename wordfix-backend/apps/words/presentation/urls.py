"""
Word URL routing.
"""

from django.urls import path

from .views import (
    AnalyzeTextView,
    CSVImportView,
    CSVValidateView,
    EnrichAllView,
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
    path("<uuid:word_id>/", WordDetailView.as_view(), name="word-detail"),
    path("<uuid:word_id>/enrich/", EnrichWordView.as_view(), name="word-enrich"),
    path("<uuid:word_id>/enrichment-status/", EnrichmentStatusView.as_view(), name="word-enrichment-status"),
    path("categories/", WordCategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<uuid:category_id>/", WordCategoryDeleteView.as_view(), name="category-delete"),
]
