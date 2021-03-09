from django.shortcuts import render
from propiedades.models import *
import random
import locale
from root.models import *
from django.shortcuts import redirect
from root.forms import TextMDForm


# Create your views here.
def home(request):
    locale.setlocale( locale.LC_ALL, '' )
    last = Propiedad.objects.filter(estado_activo = True).count()

    if last <= 0:
        return render(request, 'tachyon/homepage.html')

    # Here's one simple way to keep even distribution for
    # index2 while still gauranteeing not to match index1.

    index = []

    if last > 0:
        index1 = random.randint(0, last-1)

    if last > 1:
        index2 = random.randint(0, last-2)
        if index2 == index1:
            index2 = last-1

    if last > 2:
        index3 = random.randint(0, last-3)
        if index3 == index1:
            index3 = last-1
        if index3 == index2:
            index3 = last-2
        if index3 == index1:
            index3 = last-1

    if last > 3:
        index4 = random.randint(0, last-4)
        if index4 == index1:
            index4 = last-1
        if index4 == index2:
            index4 = last-2
        if index4 == index3:
            index4 = last-3
        if index4 == index2:
            index4 = last-2
        if index4 == index1:
            index4 = last-1
        if index4 == index2:
            index4 = last-2

    if last > 4:
        index5 = random.randint(0, last-5)
        if index5 == index1:
            index5 = last-1
        if index5 == index2:
            index5 = last-2
        if index5 == index3:
            index5 = last-3
        if index5 == index4:
            index5 = last-4
        if index5 == index3:
            index5 = last-3
        if index5 == index2:
            index5 = last-2
        if index5 == index1:
            index5 = last-1
        if index5 == index2:
            index5 = last-2
        if index5 == index3:
            index5 = last-3
        if index5 == index4:
            index5 = last-4

    index.append(index1)
    index.append(index2)
    index.append(index3)
    index.append(index4)
    index.append(index5)

    p = []

    # This syntax will generate "OFFSET=indexN LIMIT=1" queries
    # so each returns a single record with no extraneous data.


    for i in index:
        aux = Propiedad.objects.filter(estado_activo = True)[i]
        aux.precio = locale.currency(aux.precio, grouping=True)
        aux.precio = aux.precio[0:-3]
        p.append(aux)


    limit = 9

    if last < limit:
        c = last
    else:
        c = limit

    vistas = Propiedad.objects.filter(estado_activo = True).order_by('-visitas')[:c] #Set the amount of entries
    for v in vistas:
        v.precio = locale.currency(v.precio, grouping=True)
        v.precio = v.precio[0:-3]

    nuevas = Propiedad.objects.filter(estado_activo = True).order_by('-fecha_publicacion')[:c] #Set the amount of entries
    for n in nuevas:
        n.precio = locale.currency(n.precio, grouping=True)
        n.precio = n.precio[0:-3]

    if vistas and nuevas:
        return render(request, 'tachyon/homepage.html', {'properties': p, 'views': vistas, 'new': nuevas})
    else:
        raise Http404


def nosotrosView(request):
    can_edit = False
    if not request.user.is_anonymous:
        can_edit_list = ["Administrador", "SuperAdministrador", "SuperUsaurus"]
        userloggednow = TachyonUsuario.objects.get(user = request.user)
        if userloggednow.rol.nombre in can_edit_list:
            can_edit = True
    politicas = TextMD.objects.all().filter(nombre = "politicas").first()
    form = TextMDForm(instance = politicas)
    context = {'can_edit': can_edit, 'politicas':politicas, 'form':form}
    return render(request, 'root/nosotros.html', context )

def savepoliticas(request):
    politicas = TextMD.objects.all().filter(nombre = "politicas").first()
    politicas.texto = request.POST['texto']
    politicas.save()
    return redirect('nosotros')


def ayudaView(request):
    can_edit = False
    if not request.user.is_anonymous:
        can_edit_list = ["Administrador", "SuperAdministrador", "SuperUsaurus"]
        userloggednow = TachyonUsuario.objects.get(user = request.user)
        if userloggednow.rol.nombre in can_edit_list:
            can_edit = True
    ayuda = TextMD.objects.all().filter(nombre = "ayuda").first()
    form = TextMDForm(instance = ayuda)
    context = {'can_edit': can_edit, 'ayuda':ayuda, 'form':form}
    return render(request, 'root/ayuda.html', context)

def saveayuda(request):
    ayuda = TextMD.objects.all().filter(nombre = "ayuda").first()
    ayuda.texto = request.POST['texto']
    ayuda.save()
    return redirect('ayuda')
