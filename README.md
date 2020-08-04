# Wagtail Unsplash

Search for Unsplash images and upload to Wagtail

This uses the python-unsplash API wrapper:
https://github.com/yakupadakli/python-unsplash

Install with `pip install wagtail-unsplash`

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
