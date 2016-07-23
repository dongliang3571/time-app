import random

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class TemporalUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='email address', max_length=255,
                              unique=True)
    qr_code_string = models.CharField(max_length=300, null=True, blank=True)
    pin_number = models.CharField(max_length=4, null=True, blank=True)
    createAt = models.DateTimeField(verbose_name='date joined',
                                    default=timezone.now)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('session-temporalusershow', kwargs={'pk': self.pk})


def new_temporal_user_receiver(sender, instance, created, *args, **kwargs):
    """
    recevier for when a new TemporalUser is created, it will create a new
    qr_code_string for this TemporalUser
    """
    if created:
        post_save.disconnect(new_temporal_user_receiver, sender=sender)
        instance.qr_code_string = (instance.first_name
                                   + '_'
                                   + instance.last_name
                                   + str(random.randint(1, 10))
                                   + str(random.randint(1, 10))
                                   + instance.email)
        instance.save()
        post_save.connect(new_temporal_user_receiver, sender=sender)

post_save.connect(new_temporal_user_receiver, sender=TemporalUser)


###################################Session######################################
# class UserSessionQuerySet(models.QuerySet):
#     def get_sessions_for_day(self, date):
#         return
# class UserSessionManager(models.Manager):
#     def get_queryset(self):
#         return

class UserSession(models.Model):
    temporal_user = models.ForeignKey(TemporalUser)
    login_time = models.DateTimeField(verbose_name='date time logged in',
                                      null=True, blank=True)
    logout_time = models.DateTimeField(verbose_name='date time logged out',
                                       null=True, blank=True)
    is_active = models.BooleanField(verbose_name='check if session is active',
                                    default=False)
    total_minutes = models.IntegerField(default=0, null=True, blank=True)
    createAt = models.DateTimeField(verbose_name='date created',
                                    default=timezone.now)

    def __unicode__(self):
        return "{0} {1}".format(self.temporal_user.first_name,
                                self.temporal_user.last_name)

    def get_absolute_url(self):
        return reverse('session-usersessionshow', kwargs={'pk': self.pk})

    def calculate_total_minutes(self):
        total_seconds = (self.logout_time - self.login_time).total_seconds()
        self.total_minutes = total_seconds/60
        self.save()
        return self.total_minutes

    def calculate_total_minutes_now(self):
        """
        A user is able to check how many hours he has done since he logged in
        """
        total_seconds = (timezone.now() - self.login_time).total_seconds()
        return total_seconds


def new_user_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        post_save.disconnect(new_user_session_receiver, sender=sender)
        instance.is_active = True
        instance.login_time = timezone.now()
        instance.save()
        post_save.connect(new_user_session_receiver, sender=sender)

post_save.connect(new_user_session_receiver, sender=UserSession)
