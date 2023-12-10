from django.utils.translation import gettext_lazy as _
from queryish import Queryish, VirtualModel

from wagtail_unsplash.api import api

PAGE_COUNT = 30


class UnsplashQueryish(Queryish):
    page_count = PAGE_COUNT

    def run_query(self):
        if not self.offset:
            self.offset = 0

        search = False
        search_query = None
        if self.filters:
            for filter_key, filter_value in self.filters:
                if filter_key == "query":
                    search = True
                    search_query = filter_value
                    break
                if filter_key in ["id", "pk"]:
                    yield self.get_instance(api.photo.get(filter_value).__dict__)
                    return
        current_page = self.offset // self.page_count + 1
        if search:
            photos = api.search.photos(
                query=search_query,
                per_page=self.page_count,
                page=current_page,
            )["results"]
        else:
            photos = api.photo.all(
                per_page=self.page_count,
                page=current_page,
            )

        if self.limit:
            photos = photos[: self.limit]
        for photo in photos:
            yield self.get_instance(photo.__dict__)

    def get_instance(self, val):
        if self.model:
            return self.model.from_query_data(val)
        return val

    def search(self, query):
        return self.clone(filters=[("query", query)])


class UnsplashPhoto(VirtualModel):
    base_query_class = UnsplashQueryish

    class Meta:
        fields = [
            "id",
            "description",
            "alt_description",
            "urls",
            "created_at",
            "updated_at",
            "width",
            "height",
        ]

    def __str__(self):
        return self.alt_description
