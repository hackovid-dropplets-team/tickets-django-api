from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.utils.translation import ugettext as _


class Ticket(models.Model):
    title = models.CharField(verbose_name='Títol', max_length=60)
    description = models.TextField(
        verbose_name='Descripció', null=True, blank=True)
    published = models.DateTimeField(
        verbose_name='Publicat', auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, default=None)
    zip_code = models.CharField(verbose_name='Codi Postal', max_length=10, validators=[
                                RegexValidator('^\d{5}(?:[-\s]\d{4})?$')])
    # voluntary = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets_as_voluntary', related_query_name='ticket_as_voluntary', default=None)


class Dialog(TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    voluntary = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Voluntari"), on_delete=models.CASCADE)

    class Meta:
        unique_together = ['voluntary', 'ticket']

    def __str__(self):
        return _("Xat amb ") + self.opponent.username


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_(
        "Dialog"), related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages",
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Message text"))
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    all_objects = models.Manager()

    def get_formatted_create_datetime(self):
        return dj_date(localtime(self.created), settings.DATETIME_FORMAT)

    def __str__(self):
        return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"
