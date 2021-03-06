import datetime
import os

from django.contrib.messages.views import SuccessMessageMixin
from django.utils import dateformat
from django.views.generic import DetailView

from .models import ContentPage

# Create your views here.
from django_weasyprint import WeasyTemplateResponseMixin
from blog.settings import BASE_DIR, PROJECT_NAME


class ContentDetailView(SuccessMessageMixin, DetailView):
    model = ContentPage
    # def get_context_data(self, **kwargs):


class ContentDetailPrintView(ContentDetailView, WeasyTemplateResponseMixin):
    pdf_filename = dateformat.format(datetime.datetime.now(), 'd.m.Y')+'.pdf'
    # permission_required = ('content.import_content', )
    template_name = 'content/content_detail_print.html'
    # output of MyModelView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        os.path.join(BASE_DIR, PROJECT_NAME, 'static', 'css', 'weasyprint.css')
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True

    # def get_pdf_filename(self):
    #     obj = self.get_object()
    #     date = dateformat.format(datetime.datetime.now(), 'd.m.Y')
    #
    #     file_name = date+'.pdf'
    #
    #     return file_name
