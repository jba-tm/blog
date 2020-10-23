import os

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView

from .models import ContentPage

# Create your views here.
# from django_weasyprint import WeasyTemplateResponseMixin
from blog.settings import BASE_DIR, PROJECT_NAME


class ContentDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = ContentPage

    # def get_context_data(self, **kwargs):


class ContentDetailPrintView(ContentDetailView, PermissionRequiredMixin):

    permission_required = ('content.import_content', )
    template_name = 'content/content_detail_print.html'
    # output of MyModelView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        # _base.BASE_DIR + '/blog/static/css/weasyprint.css'

        os.path.join(BASE_DIR, PROJECT_NAME, 'static', 'css', 'weasyprint.css')
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True

    def get_pdf_filename(self):
        obj = self.get_object()
        file_name = obj.title+'.pdf'
        return file_name
