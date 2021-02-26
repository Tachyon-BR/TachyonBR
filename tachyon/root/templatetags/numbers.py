from django import template
import math

register = template.Library()

def myround(x, prec=1, base=.5):
  return round(base * round(float(x)/base),prec)

@register.filter
def rounding(value):
    if value.is_integer():
        return math.floor(value)
    return myround(value)
