from decimal import Decimal
import random
import pytz

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Department(models.Model):
    organization = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    createAt = models.DateTimeField(verbose_name='date created',
                                    default=timezone.now)

    def __unicode__(self):
        return self.name


class TemporalUserQuerySet(models.QuerySet):
    def get_all_for_organization(self, organization):
        return self.filter(organization=organization)

    def get_all_members_for_organization(self, organization):
        return self.filter(organization=organization, is_visitor=False)

    def get_all_visitors_for_organization(self, organization):
        return self.filter(organization=organization, is_visitor=True)


class TemporalUserManager(models.Manager):
    def get_queryset(self):
        return TemporalUserQuerySet(self.model, using=self._db)

    def get_all_for_organization(self, organization):
        return self.get_queryset().filter(organization=organization)

    def get_all_members_for_organization(self, organization):
        return self.get_queryset().get_all_members_for_organization(organization)

    def get_all_visitors_for_organization(self, organization):
        return self.get_queryset().get_all_visitors_for_organization(organization)

    def count_all_members_for_organization(self, organization):
        return self.get_all_members_for_organization(organization).count()

    def count_all_visitors_for_organization(self, organization):
        return self.get_all_visitors_for_organization(organization).count()


class TemporalUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(verbose_name='email address', max_length=255,
                              unique=True)
    organization = models.ForeignKey(User, null=True, blank=True)
    department= models.ForeignKey(Department, null=True, blank=True)
    wage = models.DecimalField(null=True,
                               blank=True,
                               max_digits=7,
                               decimal_places=2)
    qr_code_string = models.CharField(max_length=300, null=True, blank=True)
    pin_number = models.CharField(max_length=4, null=True, blank=True)
    is_visitor = models.BooleanField(default=False)
    createAt = models.DateTimeField(verbose_name='date joined',
                                    default=timezone.now)

    objects = TemporalUserManager()

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('session-memberdetail', kwargs={'pk': self.pk})


def new_temporal_user_receiver(sender, instance, created, *args, **kwargs):
    """
    recevier for when a new TemporalUser is created, it will create a new
    qr_code_string for this TemporalUser
    """
    if created:
        post_save.disconnect(new_temporal_user_receiver, sender=sender)
        instance.full_name = instance.first_name + ' ' + instance.last_name
        instance.qr_code_string = (instance.first_name
                                   + '_'
                                   + instance.last_name
                                   + str(random.randint(1, 10))
                                   + str(random.randint(1, 10))
                                   + ''.join(random.sample(instance.email,
                                                           len(instance.email)))
                                   )
        instance.save()
        post_save.connect(new_temporal_user_receiver, sender=sender)

post_save.connect(new_temporal_user_receiver, sender=TemporalUser)


###################################Session######################################
class UserSessionQuerySet(models.QuerySet):
    def get_active_sessions(self):
        return self.filter(is_active=True)

    def get_active_sessions_for_organization(self, organization):
        return self.get_active_sessions().filter(
            temporal_user__organization=organization)

    def get_active_visitors_sessions_for_organization(self, organization):
        return self.get_active_sessions().filter(
            temporal_user__organization=organization,
            temporal_user__is_visitor=True)

    def get_active_members_sessions_for_organization(self, organization):
        return self.get_active_sessions().filter(
            temporal_user__organization=organization,
            temporal_user__is_visitor=False)

    def get_inactive_sessions_for_employee(self, employee):
        return self.filter(temporal_user=employee, is_active=False)

    def get_inactive_sessions_for_start_date(self, date):
        print(date)
        UTC = pytz.timezone('UTC')
        newDate = UTC.localize(date)
        print(newDate)
        return self.filter(login_time__gte=newDate, is_active=False)

    def get_inactive_sessions_for_employee_start_date(self, employee, date):
        return self.filter(temporal_user=employee,
                           login_time__gte=date,
                           is_active=False)

    def get_inactive_sessions_for_start_date_end_date(self,
                                                      start_date,
                                                      end_date):
        return self.filter(login_time__range=(start_date, end_date),
                           is_active=False)

    def get_inactive_sessions_for_employee_start_date_end_date(self,
                                                           employee,
                                                           start_date,
                                                           end_date):
        return self.filter(temporal_user=employee,
                           login_time__range=(start_date, end_date),
                           is_active=False)


class UserSession(models.Model):
    temporal_user = models.ForeignKey(TemporalUser)
    login_time = models.DateTimeField(verbose_name='date time logged in',
                                      null=True, blank=True)
    logout_time = models.DateTimeField(verbose_name='date time logged out',
                                       null=True, blank=True)
    is_active = models.BooleanField(verbose_name='check if session is active',
                                    default=False)
    total_minutes = models.IntegerField(default=0, null=True, blank=True)
    total_salary = models.DecimalField(null=True,
                                       blank=True,
                                       max_digits=10,
                                       decimal_places=2)
    createAt = models.DateTimeField(verbose_name='date created',
                                    default=timezone.now)

    objects = UserSessionQuerySet.as_manager()

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

    def total_time_in_hours(self):
        hour = self.total_minutes/60
        return "%.1f"%(self.total_minutes/60)

    def total_time_in_hours_float(self):
        return Decimal(self.total_minutes/60.0)

    def proper_login_time_string(self):
        format = '%Y-%m-%d %H:%M:%S'
        return self.login_time.strftime(format)

    def proper_logout_time_string(self):
        format = '%Y-%m-%d %H:%M:%S'
        return self.logout_time.strftime(format)

    def proper_login_date_string(self):
        format = '%m/%d/%Y'
        return self.login_time.strftime(format)

    def proper_logout_date_string(self):
        format = '%m/%d/%Y'
        return self.logout_time.strftime(format)

    def proper_login_time_only_string(self):
        format = '%I:%M:%S %p'
        return self.login_time.strftime(format)

    def proper_logout_time_only_string(self):
        format = '%I:%M:%S %p'
        return self.logout_time.strftime(format)

    def calculate_total_salary(self):
        self.total_salary = (
            self.temporal_user.wage * self.total_time_in_hours_float()
        )
        self.save()
        return self.total_salary

    def total_salary_string(self):
        return self.total_salary

    def get_name(self):
        return self.temporal_user.full_name

def new_user_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        post_save.disconnect(new_user_session_receiver, sender=sender)
        instance.is_active = True
        instance.save()
        post_save.connect(new_user_session_receiver, sender=sender)

post_save.connect(new_user_session_receiver, sender=UserSession)
