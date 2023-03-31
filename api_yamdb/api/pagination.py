from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class CursorCountPagination(CursorPagination):
    """Назначаем поле pk как сортировку по умолчанию,
       чтобы можно было применить ко всем моделям"""
    ordering = "pk"

    def paginate_queryset(self, queryset, request, view=None):
        """Добавляет поле count в объект CursorCountPagination"""
        self.count = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """Кастомизирует ответ"""
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
