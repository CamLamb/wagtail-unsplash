# [Wagtail Unsplash](https://pypi.org/project/wagtail-unsplash/)  [![PyPI](https://img.shields.io/pypi/v/wagtail-unsplash.svg)](https://pypi.org/project/wagtail-unsplash/)

![Screenshot showing wagtail-unsplash search results](https://i.imgur.com/Va0kCys.png)

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
