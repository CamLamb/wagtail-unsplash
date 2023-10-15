# [Wagtail Unsplash](https://pypi.org/project/wagtail-unsplash/)  [![PyPI](https://img.shields.io/pypi/v/wagtail-unsplash.svg)](https://pypi.org/project/wagtail-unsplash/)

![Screenshot showing wagtail-unsplash search results](https://i.imgur.com/q12TzZL.png)

Search for Unsplash images and upload to the Wagtail image library.

This package uses the [python-unsplash](https://github.com/yakupadakli/python-unsplash) API wrapper:

## Setup

Install using pip:

```sh
pip install wagtail-unsplash
```

After installing the package, add `wagtail_unsplash` to installed apps in your settings file:

```python
# settings.py

INSTALLED_APPS = [
    ...
    'wagtail_unsplash',
    ...
]
```

and add the API credentials:

```python
# settings.py
WAGTAIL_UNSPLASH = {
    "CLIENT_ID": "",
    "CLIENT_SECRET": ""
}
```

You can get the needed information by creating an application at https://unsplash.com/developers

Make sure to define the "wagtail_unsplash" storage like so:

```python
# settings.py
STORAGES = {
    ...
    'wagtail_unsplash': {
        'BACKEND': 'wagtail_unsplash.storage.UnsplashStorage',
        "OPTIONS": {
            "location": "/wagtail_unsplash",
        },
    },
}
```

Set up a custom image model:
```python
# settings.py
WAGTAILIMAGES_IMAGE_MODEL = "home.CustomImage"

# models.py
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail_unsplash.models import UnsplashImageMixin


class CustomImage(UnsplashImageMixin, AbstractImage):
    admin_form_fields = Image.admin_form_fields


class CustomImageRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
```

<!-- Follow the **installation** steps for [wagtail-generic-chooser](https://github.com/wagtail/wagtail-generic-chooser) -->
