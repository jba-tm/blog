from .models import ContentPage


def last_contents(request):
    contents = ContentPage.objects
    return {'last_contents': contents.live().order_by('-last_published_at')[:10]}
