from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.utils.translation import ugettext_lazy as _
from wagtail.core.models import Page
from wagtail.search.models import Query


# def search(request):
# search_query = request.GET.get('query', None)
# page = request.GET.get('page', 1)
#
# # Search
# if search_query:
#     search_results = Page.objects.live().search(search_query)
#     query = Query.get(search_query)
#
#     # Record hit
#     query.add_hit()
# else:
#     search_results = Page.objects.none()
#
# # Pagination
# paginator = Paginator(search_results, 10)
# try:
#     search_results = paginator.page(page)
# except PageNotAnInteger:
#     search_results = paginator.page(1)
# except EmptyPage:
#     search_results = paginator.page(paginator.num_pages)
#
# return render(request, 'search/search.html', {
#     'search_query': search_query,
#     'search_results': search_results,
# })

class SearchView(ListView):
    template_name = 'search/search.html'
    context_object_name = 'search_results'
    paginate_by = 25

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('query', None)
        if search_query:
            self.queryset = Page.objects.live().search(search_query)
            query = Query.get(search_query)

            # Record hit
            query.add_hit()
        else:
            self.queryset = Page.objects.none()
        return super().get(request, *args, **kwargs)
