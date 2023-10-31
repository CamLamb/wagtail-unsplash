import imghdr
import os
import urllib.request

from django.conf import settings
from django.core.files import File
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from wagtail.admin.forms.search import SearchForm
from wagtail.images import get_image_model

from wagtail_unsplash.models import UnsplashPhoto


def get_search_form(request: HttpRequest) -> SearchForm:
    if 'q' in request.GET:
        return SearchForm(request.GET, placeholder=_("Search Unsplash"))
    return SearchForm(placeholder=_("Search Unsplash"))


def search_unsplash_images_index(request: HttpRequest):
    return TemplateResponse(request, 'wagtail_unsplash/search.html', {
        "search_form": get_search_form(request),
    })


def search_unsplash_images(request: HttpRequest):
    query_string = None
    search_form = get_search_form(request)
    if search_form.is_valid():
        query_string = search_form.cleaned_data['q']

    unsplash_photos = None
    if query_string:
        unsplash_photos = UnsplashPhoto.objects.search(query_string)

    context = {
        'search_form': search_form,
        'results': unsplash_photos,
    }

    return TemplateResponse(request, 'wagtail_unsplash/results.html', context)


def add_unsplash_image(request: HttpRequest):
    if request.POST and "image_id" in request.POST:
        image = add_unsplash_image_to_wagtail(request.POST["image_id"])
        return redirect(reverse("wagtailimages:edit", args=(image.id,)))
    return redirect(reverse("search_unsplash_images_index"))


def add_unsplash_image_to_wagtail(image_id):
    unsplash_photo = UnsplashPhoto.objects.get(id=image_id)
    unsplash_image = urllib.request.urlretrieve(unsplash_photo.urls.raw)
    print(unsplash_photo.urls.raw)

    # Determine the file extension
    file_extension = imghdr.what(unsplash_image[0])
    # Define a new file path in your static files directory
    new_file_path = os.path.join(
        settings.STATIC_ROOT,
        'images',
        f'{unsplash_photo.id}.{file_extension}',
    )
    # Move the temporary file to the new file path
    os.rename(unsplash_image[0], new_file_path)

    with open(new_file_path, 'rb') as fp:
        Image = get_image_model()
        image_obj = Image.objects.create(
            title=f"Unsplash image ({unsplash_photo.id})",
            file=File(fp, name=f'{unsplash_photo.id}.jpg'),
            width=unsplash_photo.width,
            height=unsplash_photo.height,
        )
        return image_obj
