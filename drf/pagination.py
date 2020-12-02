from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from drf.response import ApiResponse


class ApiPageNumberPagination(PageNumberPagination):

    def get_count(self, queryset):
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.count = self.get_count(queryset)
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):

        return ApiResponse(
            data=data,
            total=self.count
        )


class OpenApiPageNumberPagination(PageNumberPagination):

    def get_count(self, queryset):
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)

    def get_paginated_response(self, data):
        return ApiResponse(
            links={
                "first": "1",
                "last": self.max_page_number,
                "prev": self.get_previous_link(),
                "next": self.get_next_link()
            },
            meta={
                "current_page": self.current_page_number,
                "from": (int(self.current_page_number) - 1) * self.page_size + 1,
                "last_page": self.max_page_number,
                "path": self.uri,
                "per_page": self.page_size,
                "to": min(int(self.current_page_number) * self.page_size, self.max_page_number),
                "total": self.count
            },
            code=200,
            data=data
        )

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.uri = request.build_absolute_uri('?')
        self.count = self.get_count(queryset)
        page_size = self.get_page_size(request)
        self.page_size = page_size
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        self.current_page_number = page_number
        self.max_page_number = paginator.num_pages
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


