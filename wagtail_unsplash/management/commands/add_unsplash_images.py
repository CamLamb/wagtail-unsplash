from urllib.request import urlopen

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from wagtail.images import get_image_model
from wagtail_unsplash.models import UnsplashPhoto

WagtailImage = get_image_model()

class Command(BaseCommand):
    help = "Adds some unsplash images"

    def handle(self, *args, **options):
        unsplash_photos = UnsplashPhoto.objects.search("sheep")
        for unsplash_photo in unsplash_photos:
            if all(
                [
                    unsplash_photo.description,
                    unsplash_photo.urls.raw,
                    unsplash_photo.width,
                    unsplash_photo.height,
                ]
            ):
                unsplash_file = urlopen(unsplash_photo.urls.raw)
                ntf = NamedTemporaryFile(delete=True)
                ntf.write(unsplash_file.read())
                WagtailImage.objects.create(
                    title=unsplash_photo.description,
                    file=unsplash_photo.urls.raw,
                    # file=ntf,
                    width=unsplash_photo.width,
                    height=unsplash_photo.height,
                )
