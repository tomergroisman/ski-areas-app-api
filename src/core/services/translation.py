from django.utils.translation import gettext as _

from strings import texts


def i18n(str):
    return _(texts[str])
