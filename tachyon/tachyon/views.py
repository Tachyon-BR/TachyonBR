from django.shortcuts import render
from propiedades.models import *
import random
import locale

# Create your views here.
def home(request):
    locale.setlocale( locale.LC_ALL, '' )
    last = Propiedad.objects.filter(estado_activo = True).count() - 1

    index1 = random.randint(0, last)
    # Here's one simple way to keep even distribution for
    # index2 while still gauranteeing not to match index1.
    index2 = random.randint(0, last - 1)
    if index2 == index1:
        index2 = last

    index3 = random.randint(0, last - 2)
    if index3 == index1:
        index3 = last - 1
    if index3 == index2:
        index3 = last - 2

    # This syntax will generate "OFFSET=indexN LIMIT=1" queries
    # so each returns a single record with no extraneous data.
    p1 = Propiedad.objects.filter(estado_activo = True)[index1]
    p1.precio = locale.currency(p1.precio, grouping=True)
    p1.precio = p1.precio[0:-3]

    p2 = Propiedad.objects.filter(estado_activo = True)[index2]
    p2.precio = locale.currency(p2.precio, grouping=True)
    p2.precio = p2.precio[0:-3]

    p3 = Propiedad.objects.filter(estado_activo = True)[index3]
    p3.precio = locale.currency(p3.precio, grouping=True)
    p3.precio = p3.precio[0:-3]

    vistas = Propiedad.objects.filter(estado_activo = True).order_by('-visitas')[:3] #Set the amount of entries
    for v in vistas:
        v.precio = locale.currency(v.precio, grouping=True)
        v.precio = v.precio[0:-3]

    nuevas = Propiedad.objects.filter(estado_activo = True).order_by('-fecha_publicacion')[:3] #Set the amount of entries
    for n in nuevas:
        n.precio = locale.currency(n.precio, grouping=True)
        n.precio = n.precio[0:-3]

    if p1 and p2 and p3 and vistas and nuevas:
        return render(request, 'tachyon/homepage.html', {'p1': p1, 'p2': p2, 'p3': p3, 'views': vistas, 'new': nuevas})
    else:
        raise Http404
