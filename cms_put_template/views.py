from django.shortcuts import render, redirect
from django.http import HttpResponse
from cms_put_template.models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context, RequestContext, Template

# Create your views here.
# 1. Metodo para mostrar todo lo que tenemos en la basa de datos
# 2. Metodo para mostrar lo que nos pidan si lo tenemos en la base de datos
# 3. Metodo para guardar paginas

def showAll(request):
    lista = Pages.objects.all()
    #lo imprimimos con forma de lista con <li>
    if len(lista) != 0:
        respuesta = "<ul>"
        lista_pags = Pages.objects.all()
        for pag in lista_pags:
            respuesta+="<h4><li>Id: " + str(pag.id) + " | " + pag.name + " : " + pag.page + "</li></h4>"
    else :
        respuesta = "Data base is empty."

    if request.user.is_authenticated():
        respuesta += "</ul>"
        template = get_template('logged.html')
        usuario = request.user.username
        return HttpResponse(template.render(Context({'usuario': usuario, 'content': respuesta, 'text': "DATA BASE"})))
    else:
        template = get_template('notlogged.html')
        return HttpResponse(template.render(Context({'content': respuesta, 'text': "DATA BASE"})))


def showByID(request,identificador):
    try:
        page = Pages.objects.get(id=int(identificador))
        respuesta = "U chose " + page.name + ". Its page is: " + page.page + ". Its id is: " + str(page.id)
    except Pages.DoesNotExist:
        respuesta = "The page doesn't exist."
    if request.user.is_authenticated():
        template = get_template('logged.html')
        usuario = request.user.username
        return HttpResponse(template.render(Context({'usuario': usuario, 'content': respuesta})))
    else:
        template = get_template('notlogged.html')
        return HttpResponse(template.render(Context({'content': respuesta})))

@csrf_exempt
def processRequest(request,name):
    if request.method == "GET":
        try:
            page = Pages.objects.get(name=name)
            respuesta = "U chose " + page.name + ". Its page is: " + page.page + ". Its id is: " + str(page.id)
            if request.user.is_authenticated():
                template = get_template('logged.html')
                usuario = request.user.username
                return HttpResponse(template.render(Context({'usuario': usuario, 'content': respuesta})))
            else:
                template = get_template('notlogged.html')
                return HttpResponse(template.render(Context({'content': respuesta})))
        except Pages.DoesNotExist:
            template = get_template('form.html')
            return HttpResponse(template.render(Context({'text': "The page doesn't exist. Creat it."})))
    elif request.method == "PUT":
        if request.user.username: #tienes que estar logueado para guardar paginas
            try:
                pagina = Pages.objects.get(name=name)
                respuesta = "A page with that name already exists."
                template = get_template('logged.html')
                usuario = request.user.username
                return HttpResponse(template.render(Context({'usuario': usuario, 'content': respuesta})))
            except Pages.DoesNotExist:
                body = request.body.split(','); #decode('utf-8')
                #print(pagina[0])
                pagina = Pages(name=body[0], page=body[1])
                pagina.save()
                respuesta = "The page " + body[0] \
                            + " has been saved with id: " + str(pagina.id)
                template = get_template('logged.html')
                return HttpResponse(template.render(Context({'usuario': usuario,'content': respuesta})))

        else:
            template = get_template('notlogged.html')
            respuesta = "U are not logged in. U cant add pages. Log in please."
            return HttpResponse(template.render(Context({'content': respuesta})))
    elif request.method == "POST":
        if request.user.username: #tienes que estar logueado para guardar paginas
            try:
                pagina = Pages.objects.get(name=request.POST['nombre'])
                respuesta = "A page with that name already exists."
                template = get_template('logged.html')
                usuario = request.user.username
                return HttpResponse(template.render(Context({'usuario': usuario, 'content': respuesta})))
            except Pages.DoesNotExist:
                nombre = request.POST['nombre']
                pagina = request.POST['pagina']
                pagina = Pages(name=nombre, page=pagina)
                pagina.save()
                respuesta = "The page " + nombre \
                            + " has been saved with id: " + str(pagina.id)
                template = get_template('logged.html')
                usuario = request.user.username
                return HttpResponse(template.render(Context({'usuario': usuario, 'content': respuesta})))

        else:
            template = get_template('notlogged.html')
            respuesta = "U are not logged in. U cant add pages. Log in please."
            return HttpResponse(template.render(Context({'content': respuesta})))
    else :
        respuesta = "Method not Allowed"
        return HttpResponse(respuesta)

def logout(request):
    #redirigir a /admin/logout
    return redirect('/admin/logout/')
