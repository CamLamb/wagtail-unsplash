from wagtail_unsplash.settings import wagtail_unsplash_settings

from unsplash.api import Api
from unsplash.auth import Auth

api = Api(
    Auth(
        wagtail_unsplash_settings.CLIENT_ID,
        wagtail_unsplash_settings.CLIENT_SECRET,
        wagtail_unsplash_settings.REDIRECT_URI,
        code=wagtail_unsplash_settings.CODE,
    )
)
