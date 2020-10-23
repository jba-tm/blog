from django.contrib import admin
from wagtail.images.models import Image
# from wagtail.documents.models import Document
from .models import OnlineUserActivity

##################################################
# Wagtail disable Images, Documents page models #
##################################################
# admin.site.unregister(Document)
# admin.site.unregister(Image)


########################
# Online user activity #
########################


class OnlineUserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_activity',)
    search_fields = ['user__username', ]
    list_filter = ['last_activity']

    def get_ordering(self, request):
        return ['last_activity']


admin.site.register(OnlineUserActivity, OnlineUserActivityAdmin)
