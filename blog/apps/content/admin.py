from django.contrib import admin

# Register your models here.
from .models import ContentType, ContentDirection, ContentImportance, ContentCategory

admin.site.register(ContentType)
admin.site.register(ContentDirection)
admin.site.register(ContentImportance)
admin.site.register(ContentCategory)
