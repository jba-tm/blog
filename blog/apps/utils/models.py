from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from wagtail.core.models import Page


# Create your models here.

#############################
# Prevent concurrent login #
#############################

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)


class Visitor(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=False, related_name='visitor', on_delete=models.CASCADE)
    session_key = models.CharField(null=False, max_length=40)

########################
# Online user activity #
########################


class OnlineUserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    last_activity = models.DateTimeField()

    @staticmethod
    def update_user_activity(user):
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        OnlineUserActivity.objects.update_or_create(user=user, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=5)):
        """
        Gathers OnlineUserActivity objects from the database representing active users.

        :param time_delta: The amount of time in the past to classify a user as "active". Default is 15 minutes.
        :return: QuerySet of active users within the time_delta
        """
        starting_time = timezone.now() - time_delta
        return OnlineUserActivity.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')

    class Meta:
        verbose_name_plural = _('Online users activities')
        verbose_name = _('Online user activity')
        db_table = 'online_users_onlineuseractivity'


#####################
# Model soft delete #
#####################

class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=_('Deleted at'))

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()

    def filter(self):
        super().filter(self)

###########################
# Wagtail pagination page #
###########################


class PaginationPage(Page):
    is_creatable = False
    pagination_item_per_page = 25
    context_pagination_name = 'context_pages'
    pagination_query = None
    pagination_can_none = False
    pagination_order_by = '-last_published_at'

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        if self.pagination_query or (not self.pagination_query and self.pagination_can_none):
            all_pages = self.pagination_query
        else:
            all_pages = self.get_children().live().order_by(self.pagination_order_by)
        # Paginate all posts by 2 per page
        paginator = Paginator(all_pages, self.pagination_item_per_page)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            context_pages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            context_pages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            context_pages = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context[self.context_pagination_name] = context_pages
        return context

    class Meta:
        abstract = True