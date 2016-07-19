from django.db import models


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



class UserSession(models.Model):
    temporal_user = models.ForeignKey(TemporalUser)
    login_time = models.DateTimeField(verbose_name='date time logged in',
                                    default=timezone.now)
    logout_time = models.DateTimeField(verbose_name='date time logged out',
                                    default=timezone.now)
    createAt = models.DateTimeField(verbose_name='date created',
                                    default=timezone.now)

    def __unicode__(self):
        return "{0} {1}".format(self.temporal_user.first_name, self.temporal_user.last_name)
