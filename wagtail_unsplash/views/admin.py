import os
import urllib.request

from django.conf import settings
from django.core.files import File
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView
from wagtail.admin.forms.search import SearchForm
from wagtail.images import get_image_model

from wagtail_unsplash.models import UnsplashPhoto


def get_search_form(request: HttpRequest) -> SearchForm:
    if "q" in request.GET:
        return SearchForm(request.GET, placeholder=_("Search Unsplash"))
    return SearchForm(placeholder=_("Search Unsplash"))


def search_unsplash_images_index(request: HttpRequest):
    return TemplateResponse(
        request,
        "wagtail_unsplash/search.html",
        {
            "search_form": get_search_form(request),
        },
    )


class SearchUnsplashImagesView(ListView):
    model = UnsplashPhoto
    context_object_name = "results"

    def get_template_names(self) -> list[str]:
        return ["wagtail_unsplash/results.html"]

    def get_queryset(self):
        query_string = None
        search_form = get_search_form(self.request)
        if search_form.is_valid():
            query_string = search_form.cleaned_data["q"]

        if query_string:
            return UnsplashPhoto.objects.search(query_string)
        return UnsplashPhoto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = get_search_form(self.request)
        if search_form.is_valid():
            context["query_string"] = search_form.cleaned_data["q"]
        context["search_form"] = search_form
        return context


def add_unsplash_image(request: HttpRequest):
    if request.POST and "image_id" in request.POST:
        image = add_unsplash_image_to_wagtail(request.POST["image_id"])
        return redirect(reverse("wagtailimages:edit", args=(image.id,)))
    return redirect(reverse("search_unsplash_images_index"))


def add_unsplash_image_to_wagtail(image_id):
    file_extension = "jpg"

    unsplash_photo = UnsplashPhoto.objects.get(id=image_id)
    raw_url = unsplash_photo.urls.raw

    # Add &fm=jpg to the URL (updating if needed)
    raw_url_parts = urllib.parse.urlparse(raw_url)
    query_params = urllib.parse.parse_qs(raw_url_parts.query)
    query_params["fm"] = [file_extension]
    raw_url_parts = raw_url_parts._replace(
        query=urllib.parse.urlencode(query_params, doseq=True)
    )

    # Define a new file path in your static files directory
    new_file_path = os.path.join(
        settings.STATIC_ROOT,
        "images",
        f"{unsplash_photo.id}.{file_extension}",
    )

    urllib.request.urlretrieve(raw_url, new_file_path)

    with open(new_file_path, "rb") as fp:
        Image = get_image_model()
        image_file = File(fp, name=f"{unsplash_photo.id}.{file_extension}")
        image_obj = Image.objects.create(
            title=f"Unsplash image ({unsplash_photo.id})",
            file=image_file,
            width=unsplash_photo.width,
            height=unsplash_photo.height,
        )
        return image_obj
