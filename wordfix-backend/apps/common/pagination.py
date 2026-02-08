"""
Custom pagination classes for WordFix API.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    """
    Standard pagination with 20 items per page.

    Includes meta information in the response:
    - page: current page number
    - total_pages: total number of pages
    - total_count: total number of items
    - page_size: items per page
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "success": True,
                "data": data,
                "message": "Success",
                "errors": None,
                "meta": {
                    "page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "total_count": self.page.paginator.count,
                    "page_size": self.get_page_size(self.request),
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )
