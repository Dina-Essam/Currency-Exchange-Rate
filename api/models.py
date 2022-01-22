from django.core.validators import RegexValidator
from django.db import models


# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=60)
    symbol = models.CharField(max_length=3,
                              validators=[RegexValidator('^[A-Z]*$', 'Only uppercase letters allowed.')])
    rates = models.ManyToManyField(
        "self",
        through='ExchangeRate',
        through_fields=('From', 'To'),
    )

    class Meta:
        ordering = ['symbol']

    def __str__(self):
        return self.name + " " + self.symbol


class ExchangeRate(models.Model):
    To = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="CurrencyTo")
    From = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="CurrencyFrom")
    date = models.DateField()
    rate = models.DecimalField(max_digits=12, decimal_places=6)

    class Meta:
        ordering = ['From']

    def __str__(self):
        return self.From.symbol + " exchange to " + self.To.symbol+" by rate "+str(self.rate) + " on "+str(self.date)



