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


    banner = 5

    if last < banner:
        banner = last

    properties = list(Propiedad.objects.filter(estado_activo = True))

    p = random.sample(properties, banner)


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
