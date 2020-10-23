from wagtail.core import hooks

from django.contrib.auth.models import Permission


@hooks.register('register_permissions')
def import_content_page():
    return Permission.objects.filter(codename='import_content')
