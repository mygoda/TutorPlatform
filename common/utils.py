# -*- coding: utf-8 -*-
# ___author__ = 'gwx'
from rest_framework import pagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except:
            raise ValidationError({"messages": "INVALID_PAGE"})
        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_data(self, data):
        return {
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'has_next': self.page.paginator.num_pages > self.page.number,
            'count': self.page.paginator.count,
            'results': data
        }

    def get_paginated_response(self, data):
        return Response(self.get_paginated_data(data))

    def get_paginated_response_with_ext(self, data, **kwargs):
        data = self.get_paginated_data(data)
        if kwargs:
            data.update(**kwargs)
        return data