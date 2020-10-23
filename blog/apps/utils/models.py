from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

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
