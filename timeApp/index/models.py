from django.db import models

# Create your models here.

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=4000)

    def __unicode__(self):
        return "name:" + str(self.name) + "email:" + str(self.email)

class Newsletter(models.Model):
    email = models.EmailField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "email is %s" %(self.email)
