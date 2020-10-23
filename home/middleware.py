from .models import HomePage


def get_menu_items(request):
    return {'home_page': HomePage.objects.get()}
