from django.urls import path, reverse_lazy
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtail_unsplash.views.admin import (
    SearchUnsplashImagesView,
    add_unsplash_image,
    search_unsplash_images_index,
)


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(
            "unsplash-search/",
            search_unsplash_images_index,
            name="search_unsplash_images_index",
        ),
        path(
            "unsplash-search/results/",
            SearchUnsplashImagesView.as_view(),
            name="search_unsplash_images",
        ),
        path(
            "unsplash-search/add-image/",
            add_unsplash_image,
            name="add_unsplash_image",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_search_unsplash_images_admin_menu_item():
    return MenuItem(
        "Unsplash Images",
        reverse_lazy("search_unsplash_images_index"),
        icon_name="image",
    )
