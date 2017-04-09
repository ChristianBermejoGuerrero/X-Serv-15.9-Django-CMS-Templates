from django.conf.urls import patterns, include, url
from django.contrib import admin
from cms_put_template import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^login$', login, name='log in'),
    url(r'^logout$', logout, name='log out'),
    url(r'^annotated$', views.showAll, name='mostrar todo'),
    url(r'^annotated/(\d+)$', views.showByID, name='mostrar si me dan ID'),
    url(r'^admin', include(admin.site.urls)),
    url(r'^annotated/(.+)', views.processRequest, name='procesar la peticion recibida'),
)
