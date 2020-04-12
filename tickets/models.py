from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


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


class Volunteering(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'ticket']
