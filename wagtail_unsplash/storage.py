from urllib.request import urlopen

from django.utils import timezone
from django.utils.functional import cached_property
from django.core.files.storage import Storage, FileSystemStorage
from django.core.files.temp import NamedTemporaryFile

from wagtail_unsplash.models import UnsplashPhoto

class UnsplashStorageMixin:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self._location = kwargs["location"]
        super().__init__(*args, **kwargs)

    @cached_property
    def unsplash_photo(self, name):
        return UnsplashPhoto.objects.get(id=name)

    def unsplash_bytes(self, name):
        return urlopen(name).read()

    def open(self, name, mode="rb"):
        ntf = NamedTemporaryFile(delete=True)
        ntf.write(self.unsplash_bytes(name))
        return ntf

    def save(self, name, content, max_length=None):
        return name

    def get_valid_name(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        return name

    def generate_filename(self, filename):
        return filename

    def delete(self, name):
        return None

    def exists(self, name):
        return True

    def listdir(self, path):
        return [], []

    def size(self, name):
        return len(self.unsplash_bytes(name))

    def url(self, name):
        return name

    def get_accessed_time(self, name):
        return timezone.now()

    def get_created_time(self, name):
        return timezone.datetime.strptime(
            self.unsplash_photo.created_at,
            "%Y-%m-%dT%H:%M:%S%z",
        )

    def get_modified_time(self, name):
        return timezone.datetime.strptime(
            self.unsplash_photo.updated_at,
            "%Y-%m-%dT%H:%M:%S%z",
        )


class UnsplashFileSystemStorage(UnsplashStorageMixin, FileSystemStorage):
    pass