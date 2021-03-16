from django import template
import math
import locale
import os

register = template.Library()

def myround(x, prec=1, base=.5):
  return round(base * round(float(x)/base),prec)

@register.filter
def rounding(value):
    if value.is_integer():
        return math.floor(value)
    return myround(value)


@register.filter
def truncate_string(value):
    return (value[:280] + '...') if len(value) > 283 else value


@register.filter
def money(value):
    locale.setlocale( locale.LC_ALL, '' )
    precio = locale.currency(value, grouping=True)
    precio = precio[0:-3]
    return precio


@register.filter
def filename(value):
    return os.path.basename(value)
