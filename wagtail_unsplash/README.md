# Wagtail Unsplash

This uses the python-unsplash API wrapper:
https://github.com/yakupadakli/python-unsplash

Add the following settings to your django settings file:

```
INSTALLED_APPS = [
    ...
    'wagtail_unsplash',
    ...
]

...

WAGTAIL_UNSPLASH = {
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "REDIRECT_URI": "",
    "CODE": "",
}
```

You can get the needed information by creating an application here:
https://unsplash.com/developers


## Examples

```
from wagtail_unsplash.api import api

api.search.photos("Search Query")
api.photo.get("Photo ID")
```

## Goals

 - Can search unsplash images in the Wagtail Image upload modal
 - Can use an unsplash image in exactly the same way as a Wagtail Image
