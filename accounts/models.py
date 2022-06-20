from django.db import models
from django.contrib.auth.models import User
from admin_panel.models import AdminUser
from django.utils.translation import ugettext_lazy as _



class Timesheet(models.Model):
    """ Timesheet model """
    LOGGING_CHOICES = (('IN', _('In')), ('OUT', _('Out')))
    # employee who recorded
    employee = models.ForeignKey(AdminUser, related_name="%(app_label)s_%(class)s_employee", on_delete=models.CASCADE)
    recorded_by = models.ForeignKey(AdminUser, related_name="%(app_label)s_%(class)s_recorded_by", on_delete=models.CASCADE)
    recorded_datetime = models.DateField(auto_now_add=True)
    clocking_time = models.DateTimeField()
    # whether the user has clocked in or out
    logging = models.CharField(max_length=3, choices=LOGGING_CHOICES)
    ip_address = models.GenericIPAddressField()
    comments = models.TextField(blank=True, null=True)
    clock_in_time = models.TimeField(blank=True, null=True)
    clock_out_time = models.TimeField(blank=True, null=True)
    status = models.BooleanField(null=True)

    class Meta:
        get_latest_by = 'clocking_time'

    def __unicode__(self):
        return "%s checked %s at %s" % (self.employee, self.logging, self.clocking_time)

    def __str__(self):
        return f'{self.employee or ""}'

