from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class CursorCountPagination(CursorPagination):
    ordering = "pk"  # set pk to fit all models

    def paginate_queryset(self, queryset, request, view=None):
        self.count = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
