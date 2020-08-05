import json
import os
import urllib.request

from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _

from wagtail.admin.forms.search import SearchForm
from wagtail.images import get_image_model

from wagtail_unsplash.api import api
from wagtail_unsplash.paginator import UnsplashPaginator

Image = get_image_model()


def search_unsplash_images(request):

    if request.POST:
        if "image_id" in request.POST:
            image = add_unsplash_image_to_wagtail(request.POST["image_id"])
            return redirect(reverse("wagtailimages:edit", args=(image.id,)))

    query_string = None
    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search Unsplash"))
        if form.is_valid():
            query_string = form.cleaned_data['q']
    else:
        form = SearchForm(placeholder=_("Search Unsplash"))

    page = int(request.GET.get("p", 1))
    per_page = 25

    images = None
    if query_string:
        paginator = UnsplashPaginator(query_string, per_page)
        images = paginator.get_page(request.GET.get('p'))

    context = {
        'search_form': form,
        'images': images,
    }

    return TemplateResponse(request, 'wagtail_unsplash/search.html', context)


def add_unsplash_image_to_wagtail(image_id):
    photo = api.photo.get(image_id)

    url = photo.urls.raw
    unsplash_image = urllib.request.urlretrieve(url)
    fname = os.path.basename(url)

    with open(unsplash_image[0], 'rb') as fp:
        image_obj = Image.objects.create(
            title=f"Unsplash image ({photo.id})",
            file=File(fp),
            width=photo.width,
            height=photo.height,
        )
        return image_obj
