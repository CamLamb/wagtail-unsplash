import collections.abc

from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail_unsplash.api import api

class UnsplashPaginator:
    """
    Based on django.core.paginator.Paginator
    """
    _response = None
    _total_pages = None
    _total_results = None

    def __init__(self, query_string, per_page):
        self.query_string = query_string
        self.per_page = int(per_page)
    
    def __iter__(self):
        for page_number in self.page_range:
            yield self.page(page_number)
    
    def run_query(self):
        if not self._response:
            self._response = api.search.photos(query=self.query_string, page=1, per_page=self.per_page)
            self._total_pages = int(self._response['total_pages'])
            self._total_results = int(self._response['total'])
    
    def validate_number(self, number):
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage(_('That page contains no results'))
        return number

    def get_page(self, number):
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return self.page(number)

    def page(self, number):
        number = self.validate_number(number)
        return self._get_page(number, self)
    
    def _get_page(self, *args, **kwargs):
        return UnsplashPage(*args, **kwargs)

    @cached_property
    def count(self):
        if self._total_results is None:
            self.run_query()
        return self._total_results

    @cached_property
    def num_pages(self):
        if not self._total_pages:
            self.run_query()
        return self._total_pages

    @property
    def page_range(self):
        return range(1, self.num_pages + 1)


class UnsplashPage(collections.abc.Sequence):
    """
    Based on django.core.paginator.Page
    """
    _response = None
    _total_pages = None
    _total_results = None

    def __init__(self, number, paginator):
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        if not self._total_results or not self._total_pages or not self.paginator.per_page:
            self.run_page_query()
        
        if self.has_next():
            return self.paginator.per_page

        return self._total_results - ((self._total_pages - 1) * self.paginator.per_page)

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                'Page indices must be integers or slices, not %s.'
                % type(index).__name__
            )
        return self._response["results"][index]

    def run_page_query(self):
        if not self._response:
            self._response = api.search.photos(query=self.paginator.query_string, page=self.number, per_page=self.paginator.per_page)
            self._total_pages = int(self._response['total_pages'])
            self._total_results = int(self._response['total'])

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def start_index(self):
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page
