from django.utils.translation import gettext_lazy as _
from django.core.files.storage import storages

from wagtail.images.models import WagtailImageField, get_upload_to, AbstractImage, AbstractRendition
from queryish import VirtualModel, Queryish
from wagtail_unsplash.api import api


class UnsplashQueryish(Queryish):
    page_count = 30

    def run_query(self):
        if self.ordering:
            print("ordering", self.ordering)

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
            photos = photos[:self.limit]
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


class UnsplashImageField(WagtailImageField):
    _storage = None

    @property
    def storage(self):
        return storages["wagtail_unsplash"]

        wagtail_unsplash_storage = storages["wagtail_unsplash"]
        print("")
        if wagtail_unsplash_storage.location in getattr(self, self.attname).path:
            return wagtail_unsplash_storage
        return self._storage

    @storage.setter
    def storage(self, value):
        self._storage = value



class UnsplashImageMixin:
    file = UnsplashImageField(
        verbose_name=_("file"),
        upload_to=get_upload_to,
        width_field="width",
        height_field="height",
    )
