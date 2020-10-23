from django.utils.translation import ugettext_lazy as _
from wagtail.core.models import Page


class HomePage(Page):
    max_count_per_parent = 0

    class Meta:
        verbose_name = _('Home')

