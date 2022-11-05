from curses import flash
from dataclasses import field
from tkinter import Widget
from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm, Form
from django.urls import reverse_lazy

from django.http.response import HttpResponseRedirect, HttpResponse

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, DetailView,TemplateView
from django.views.generic.list import ListView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Equipo, Participante,Partido,Clasificado, Penca,Torneo, Grupo
from .forms import Clasificado_form, ClasificadoUPD_form, Equipo_form, Participante_form, Partido_Form, ListaPartido_form, Penca_form, PencaConfig_form, PencaUpd_form, Torneo_Form, Fixture_form

############################################################## HOMES
class HomeView(LoginRequiredMixin,TemplateView):
    context_object_name = "home_general"
    template_name       = "torneos/home.html" 
    

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['pencas']        = Penca.objects.filter(administrador=self.request.user)    
        context['participantes'] = Participante.objects.filter(usuario=self.request.user)
    #    context['torneos']      = Torneo.objects.all()
    #    context['equipos']      = Equipo.objects.all()
    #    context['clasificados'] = Clasificado.objects.all()
    #    context['partidos']     = Partido.objects.all()
        #contex['tareas'] -> importante apuntar al context_object_name que se quiere
        #filter(tarea_usario=self.request.user) -> importante, seleccionar attributo a filtrar definido en models. para la clase en la que se esta trabajando
        #context['partidos'] = context['partidos'].filter(Partido_usario=self.request.user)
        #context['count'] = context['tareas'].filter(tarea_completada=False).count()
        return context

class PencaHome(LoginRequiredMixin,DetailView):
    model = Penca
    context_object_name = 'penca'
    template_name = "torneos/penca_home.html"

    def get_form_kwargs(self):
            kwargs = super(PencaHome, self).get_form_kwargs()
            kwargs.update({
                            'pk': self.kwargs['pk'],
                         })
            return kwargs

    def get_initial(self):
        initial = super(PencaHome, self).get_initial()
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        for participante in  Participante.objects.filter(penca = self.object).filter(usuario=self.request.user):
            print('participante ===>>>', participante.usuario)
            print('torneo_hijo  ===>>>', participante.torneo_hijo)
            context['torneohijo'] = participante.torneo_hijo
       #context['torneohijo']    = Torneo.objects.filter(id=participante.torneo_hijo)
        context['participantes'] = Participante.objects.filter(penca = self.object)
        return context   






############################################################## USUARIO

class CustomLoginView(LoginView):
    template_name               = "torneos/login.html"
    fields                      = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class AltaUsuario(FormView):   
    template_name               = "torneos/alta_usuario.html"        
    form_class                  = UserCreationForm
    redirect_authenticated_user = True
    success_url                 = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(AltaUsuario, self).form_valid(form)    

    def get(self, *args, **kargs): #hace que un usuario registrado no pueda acceder al formulario de alta usuario
        if self.request.user.is_authenticated:
            return redirect('tasks')  
        return super(AltaUsuario, self).get(*args, **kargs)      

############################################################## PARTICIPANTE

class AltaParticipante(LoginRequiredMixin, CreateView):
    model           = Participante
    form_class      = Participante_form
    template_name   = "torneos/ABM_participantes/participante_alta.html"
    success_url     = reverse_lazy('penca_home')
    def get_form_kwargs(self):
            kwargs = super(AltaParticipante, self).get_form_kwargs()

            return kwargs

    def get_initial(self):
        initial = super(AltaParticipante, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('penca_id'),} )
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
       # context['equipo'] = filtraEquipo(self.object))
        context['penca'] = self.kwargs.get('penca_id')

        return context
    
    def form_valid(self, form):
        form.instance.penca = Penca.objects.get(id=self.kwargs['penca_id'])
        return super(AltaParticipante, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('penca_home', kwargs={'pk': self.kwargs['penca_id']})            

class UpdParticipante(LoginRequiredMixin, UpdateView):
    model           = Participante
    form_class      = Participante_form
    #fields          = "__all__"
    template_name   = "torneos/ABM_participantes/participante_alta.html"
    success_url     = reverse_lazy('penca_home')


    def get_success_url(self):
        return reverse_lazy('penca_home', kwargs={'pk': self.kwargs['penca_id']})  

class DltParticipante(LoginRequiredMixin, DeleteView):
    model           = Participante
    fields          = "__all__"
    template_name   = "torneos/ABM_participantes/participante_baja.html"
    success_url     = reverse_lazy('penca_home')
    
    def get_success_url(self):
        return reverse_lazy('penca_home', kwargs={'pk': self.kwargs['penca_id']})    
############################################################## PENCA

class AltaPenca(LoginRequiredMixin, CreateView):
    model           = Penca
    form_class      = Penca_form
   
    template_name   = "torneos/ABM_Pencas/penca_alta.html"
    success_url     = reverse_lazy('home')

    def get_initial(self):
        initial = super(AltaPenca, self).get_initial()
        initial.update({ 'pk' : self.request.user.pk })
        return initial

    def form_valid(self, form): # Valido que tenga bandera, sino asigno una por defecto
        #Participante.objects.create(penca=self.object,torneo_hijo=form.instance.torneo)
        return super(AltaPenca, self).form_valid(form)

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 

        return context    

class UpdPenca(LoginRequiredMixin, UpdateView):
    model           = Penca
    form_class      = PencaUpd_form
    
    template_name   = "torneos/ABM_Pencas/penca_alta.html"
    success_url     = reverse_lazy('home')
    

    def form_valid(self, form):

        return super(UpdPenca, self).form_valid(form)

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['penca'] = self.object
        return context    
        
class DltPenca(LoginRequiredMixin, DeleteView):
    model           = Penca
    
    template_name   = "torneos/ABM_Pencas/penca_baja.html"
    success_url     = reverse_lazy('equipos')

class PencaConfig(LoginRequiredMixin,DetailView):
    model               = Penca
    form_class          = PencaConfig_form
    context_object_name = 'penca_config'
    template_name       = "torneos/penca_config.html"

    def get_form_kwargs(self):
        kwargs = super(PencaHome, self).get_form_kwargs()
        kwargs.update({
                        'pk': self.kwargs['pk'],
                        })
        print('get kwargs', kwargs)
        return kwargs

    def get_initial(self):
        initial = super(PencaHome, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('pk'),} )
        print('initial ', initial)
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
 
        context['participantes'] = Participante.objects.filter(penca = self.object)
        return context     


############################################################## Equipo

class AltaEquipo(LoginRequiredMixin, CreateView):
    model           = Equipo
    form_class      = Equipo_form
   
    template_name   = "torneos/ABM_equipos/equipo_alta.html"
    success_url     = reverse_lazy('equipos')

    def form_valid(self, form): # Valido que tenga bandera, sino asigno una por defecto
        if not form.instance.bandera:
            form.instance.bandera = 'equipos_foto/default.png'      
        return super(AltaEquipo, self).form_valid(form)

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 

        return context    

class UpdEquipo(LoginRequiredMixin, UpdateView):
    model           = Equipo
    form_class      = Equipo_form
    
    template_name   = "torneos/ABM_equipos/equipo_alta.html"
    success_url     = reverse_lazy('equipos')
    

    def form_valid(self, form):

        return super(UpdEquipo, self).form_valid(form)

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['equipo'] = self.object
        return context    
        
class DltEquipo(LoginRequiredMixin, DeleteView):
    model           = Equipo
    
    template_name   = "torneos/ABM_equipos/equipo_baja.html"
    success_url     = reverse_lazy('equipos')
        
class ListaEquipos(LoginRequiredMixin, ListView):
    model               = Equipo
    context_object_name = "equipos"
    template_name       = "torneos/lista_equipos.html"

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        #contex['tareas'] -> importante apuntar al context_object_name que se quiere
        #filter(tarea_usario=self.request.user) -> importante, seleccionar attributo a filtrar definido en models. para la clase en la que se esta trabajando
        ''' context['tareas'] = context['tareas'].filter(tarea_usario=self.request.user)
        context['count'] = context['tareas'].filter(tarea_completada=False).count()'''

        #logica del buscardor
        search_input = self.request.GET.get('objeto_buscado') or ''
        if search_input:
            context['equipos'] = context['equipos'].filter(nombre__icontains=search_input)
        context['search_input'] = search_input
        return context

############################################################## Clasificado

class AltaClasificado(LoginRequiredMixin, CreateView):
    model           = Clasificado
    form_class      = Clasificado_form
    template_name   = "torneos/ABM_clasificados/clasificado_A.html"
    success_url     = reverse_lazy('torneo_home')
    def get_form_kwargs(self):
            kwargs = super(AltaClasificado, self).get_form_kwargs()

            return kwargs
    def get_initial(self):
        initial = super(AltaClasificado, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('torneo_id'),} )
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
       # context['equipo'] = filtraEquipo(self.object))
        context['torneo'] = self.kwargs.get('torneo_id')

        return context
    
    def form_valid(self, form):
        form.instance.torneo = Torneo.objects.get(id=self.kwargs['torneo_id'])
        return super(AltaClasificado, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['torneo_id']})            

class UpdClasificado(LoginRequiredMixin, UpdateView):
    model           = Clasificado
    form_class      = ClasificadoUPD_form
    #fields          = "__all__"
    template_name   = "torneos/ABM_clasificados/clasificado.html"
    success_url     = reverse_lazy('torneo_home')


    def get_success_url(self):
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['torneo_id']})  

class DltClasificado(LoginRequiredMixin, DeleteView):
    model           = Clasificado
    fields          = "__all__"
    template_name   = "torneos/ABM_clasificados/desclasificado.html"
    success_url     = reverse_lazy('torneo_home')
    
    def get_success_url(self):
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['torneo_id']})    
        
class ListaClasificado(LoginRequiredMixin, ListView):
    model               = Clasificado
    context_object_name = "clasificados"
    template_name       = "torneos/lista_clasificados.html"
    
    def get_form_kwargs(self):
            kwargs = super(AltaClasificado, self).get_form_kwargs()

            return kwargs
    
    def get_initial(self):
        initial = super(AltaClasificado, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('torneo_id'),} )
        return initial
    
    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['torneo']       = self.kwargs.get('torneo_id')
       # print('torneo en context ======>>>>', context['torneo'])

       # torneo = Torneo.objects.filter(id=context['torneo'])
       # print('torneo ======>>>>', context['torneo'])

       # lista_clasificados = Arma_Grupos(torneo, Grupos)
       # context['participantes'] = Clasificado.objects.filter(torneo=torneo) 
       # print('lista_clasificados  ======>>>>', context['participantes'] )
        
       # if len(context['participantes']) < torneo.cntequipos and len(context['participantes']) > 0 :   
       #     context['hay_cupos'] = True 
       # else:
       #     context['hay_cupos'] = False

        #logica del buscardor
        search_input = self.request.GET.get('objeto_buscado') or ''
        if search_input:
            context['equipos'] = context['equipos'].filter(nombre__icontains=search_input)
        context['search_input'] = search_input
        return context 
        
############################################################## Torneo

def AltaTorneo_view(request):
    form            = Torneo_Form(request.POST or None)
    template_name   = "torneos/ABM_torneos/torneo_alta.html"
    context         = {
                        'form': form,
                      }  
    if request.POST and form.is_valid(): 
        print(request.POST) 
        form.full_clean()  
        torneo = form.save()
        torneo.save()
        return redirect("torneos")
    return render(request,template_name, context)

class UpdTorneo(LoginRequiredMixin, UpdateView):
    model           = Torneo
    fields          = '__all__'
    template_name   =  "torneos/ABM_torneos/torneo_alta.html"
    success_url     = reverse_lazy('torneo_home')

    def get_success_url(self):
        print('get_success_url =======>>>>>>> ',self.kwargs)
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['pk']})  

class DltTorneo(LoginRequiredMixin, DeleteView):
    model           = Torneo
    fields          = "__all__"
    template_name   = "torneos/ABM_torneos/torneo_dlt.html"
    success_url     = reverse_lazy('torneos')
    

class ListaTorneo(LoginRequiredMixin, ListView):
    model               = Torneo
    context_object_name = "torneos"
    template_name       = "torneos/lista_torneos.html"

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        #contex['tareas'] -> importante apuntar al context_object_name que se quiere
        #filter(tarea_usario=self.request.user) -> importante, seleccionar attributo a filtrar definido en models. para la clase en la que se esta trabajando
        #context['partidos'] = context['partidos'].filter(Partido_usario=self.request.user)
        #context['count'] = context['tareas'].filter(tarea_completada=False).count()
        return context

class TorneoDetalle(LoginRequiredMixin,DetailView):

    model = Torneo
    context_object_name = 'torneo'
    template_name = "torneos/torneo_home.html"

    def get_initial(self):
        initial = super(TorneoDetalle, self).get_initial()
        return initial

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Torneo.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context                  = super().get_context_data(**kwargs)
        context['torneo']        = self.object
        actualiza_ranking(self.object)
        Playoff_asigna_equipos(self.object)
        context['equipos_grupo'] = Arma_Grupos(self.object)
        context['partidos']      = torneo_fixture(self.object)
        context['fixture']       = torneo_fixture(self.object)

        return context

#Busca y ordena los partidos segun las faces del torneo
def torneo_fixture(torneo):
    partidos = [] 
    partidos_grupo = []
    playoff = (torneo.clasificanXgrupo * torneo.grupos) / 2
    x = 0
    #cargo encuentros fase grupos
    for grupo in Grupo.objects.filter(toreno=torneo):
        partidos_grupo.append(grupo.nombre)
#        print('grupos =====>>>>>>',grupo.nombre)
        
        for partido in Partido.objects.filter(torneo=torneo):
            etapa = partido.codigo.split('_',1) 
            if etapa[0] == grupo.nombre:            
                partidos_grupo.append(partido)
        if len(partidos_grupo)>1:        
            partidos.append(partidos_grupo)
        partidos_grupo = []
        x += 1

    #cargo encuentros playoff
    
    while playoff >=0:
        partidos_grupo.append(str(int(playoff)))
        for partido in Partido.objects.filter(torneo=torneo):
            etapa = partido.codigo.split('_',1) 
            if etapa[0] == str(int(playoff)):            
                partidos_grupo.append(partido)
        if len(partidos_grupo)>1:        
            partidos.append(partidos_grupo)
        partidos_grupo = []
        
        if playoff > 1:  
            playoff = playoff / 2 
        else:
            playoff -= 1
    return partidos   

#busca grupos en los que hay equipos clasificados, si en algun grupo no hay equipos no lo muestra.
def Arma_Grupos(torneo):    
    grupo_equipos = []
    lista_grupos = [] 
    x = 0 
    for grupo in Grupo.objects.filter(toreno=torneo):
        grupo_equipos = []
        grupo_equipos.append(grupo.nombre)
        for clasificado in  Clasificado.objects.filter(torneo=torneo).filter(grupo=grupo): #obtengo todos los clasificados a ese grupo
            #if clasificado.grupo == Grupos[x][0]:
                grupo_equipos.append(clasificado)
        if len(grupo_equipos)>1:       
            lista_grupos.append(grupo_equipos)
        x += 1         
    return lista_grupos

#Busca y arma el Ranking para la fase de gruupos

def Playoff_asigna_equipos(torneo):
    if torneo.fase == 'Grupos' or torneo.fase == 'Pendiente':
        # obtengo clasificados por gurpo
        for grupo in Grupo.objects.filter(toreno=torneo):    
            asignados = 1
            for clasificado in Clasificado.objects.filter(torneo=torneo).filter(grupo=grupo).order_by('-puntos'):
                if clasificado.jugados > 0:
                    if asignados == 1:
                        codigo_partido = str(int(asignados)) + grupo.nombre + " vs "
                    else:                 
                        codigo_partido = " vs "+ str(int(asignados)) + grupo.nombre
                    for partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=codigo_partido):
                        if asignados // 2:
                            partido.local = clasificado.equipo
                        else:
                            partido.visitante = clasificado.equipo
                        partido.save()        
                    asignados += 1
                    if asignados > torneo.clasificanXgrupo:
                        break
                    
        #busco en los playoff 
        playoff = (torneo.clasificanXgrupo * torneo.grupos) / 2
        while playoff >=0:
            codigo_playoff = str(int(playoff))+"_"
            print(str(int(playoff)))
            if playoff > 2: #en SEMIFINAL cambia la logica
                for partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=codigo_playoff).exclude(resultado='P'):
                    codigo_partido = partido.codigo.split(" ",1)     
                    prox_codigo    = codigo_partido[0] + " vs " 
                    encontre = False
                    for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                        encontre = True
                        if partido.resultado == 'L':
                            prox_partido.local = partido.local
                        if partido.resultado == 'V':
                            prox_partido.local = partido.visitante    
                        prox_partido.save()    
                    if not encontre:
                        prox_codigo    = " vs " + codigo_partido[0]
                        for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                            encontre = True
                            if partido.resultado == 'L':
                                prox_partido.visitante = partido.local
                            if partido.resultado == 'V':
                                prox_partido.visitante = partido.visitante    
                            prox_partido.save()    
            if playoff == 2:
                for partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=codigo_playoff).exclude(resultado='P'):
                    if partido.resultado == 'L':
                        #ganador va a la final
                        codigo_partido = partido.codigo.split(" ",1)     
                        prox_codigo    =  "0_1 "+codigo_partido[0] + " vs "      
                        encontre = False
                        for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                            encontre = True                            
                            prox_partido.local = partido.local  
                            prox_partido.save()    
                        if not encontre:
                            prox_codigo    = "0_1 "
                            for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                                encontre = True
                                prox_partido.visitante = partido.local   
                                prox_partido.save()
                        #perdedor va por 3er y 4to 
                        prox_codigo    =  "1_1 "+codigo_partido[0] + " vs "      
                        encontre = False
                        for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                            encontre = True                            
                            prox_partido.local = partido.visitante   
                            prox_partido.save()    
                        if not encontre:
                            prox_codigo    = "1_1 "
                            for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                                encontre = True
                                prox_partido.visitante = partido.visitante   
                                prox_partido.save()
                    if partido.resultado == 'V':               
                        #ganador va a la final
                        codigo_partido = partido.codigo.split(" ",1)     
                        prox_codigo    =  "0_1 "+codigo_partido[0] + " vs "      
                        encontre = False
                        for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                            encontre = True                            
                            prox_partido.local = partido.visitante 
                            prox_partido.save()    
                        if not encontre:
                            prox_codigo    = "0_1 "
                            for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                                encontre = True
                                prox_partido.visitante = partido.visitante  
                                prox_partido.save()
                        #perdedor va por 3er y 4to 
                        prox_codigo    =  "1_1 "+codigo_partido[0] + " vs "      
                        encontre = False
                        for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                            encontre = True                            
                            prox_partido.local = partido.local                                                      
                            prox_partido.save()    
                        if not encontre:
                            prox_codigo    = "1_1 "
                            for prox_partido in Partido.objects.filter(torneo=torneo).filter(codigo__icontains=prox_codigo):
                                encontre = True
                                prox_partido.visitante = partido.local                            
                                prox_partido.save()
            if playoff > 1:  
                playoff = playoff / 2 
            else:
                playoff -= 1

############################################################## Partido
 
 
class AltaPartido(LoginRequiredMixin, CreateView):
    model           = Partido
    form_class      = Partido_Form
    template_name = "torneos/ABM_partidos/partido_alta.html"
    success_url     = reverse_lazy('torneo_home')
    
    def get_form_kwargs(self):
            kwargs = super(AltaPartido, self).get_form_kwargs()
            kwargs.update({
                            'pk': self.kwargs['torneo_id'],
                         })
            return kwargs

    def get_initial(self):
        initial = super(AltaPartido, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('torneo_id'),} )
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['torneo'] = self.kwargs.get('torneo_id')
       # context['equipo'] = filtraEquipo(self.object))
       # context['torneo'] = context['torneo'].filter(torneo=self.torneo)     
        return context
    
    def form_valid(self, form):
        form.instance.torneo = Torneo.objects.get(id=self.kwargs['torneo_id'])
        return super(AltaPartido, self).form_valid(form)

    def get_success_url(self):
       # print('get_success_url =======>>>>>>> ',self.kwargs)
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['torneo_id']})    

class UpdPartido(LoginRequiredMixin, UpdateView):
    model           = Partido
    form_class      = Partido_Form
    template_name   = "torneos/ABM_partidos/partido_alta.html"
    success_url     = reverse_lazy('torneo_home')


    def get_form_kwargs(self):
            kwargs = super(UpdPartido, self).get_form_kwargs()
            kwargs.update({
                            'pk': self.kwargs['torneo_id'],
                         })
            return kwargs

    def get_initial(self):
        initial = super(UpdPartido, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('torneo_id'),} )
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['torneo'] = self.kwargs.get('torneo_id')
       # context['equipo'] = filtraEquipo(self.object))
       # context['torneo'] = context['torneo'].filter(torneo=self.torneo)     
        return context


    def get_success_url(self):
       # print('get_success_url =======>>>>>>> ',self.kwargs)
        #actualiza_ranking(self.object)
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['torneo_id']})  

class DltPartido(LoginRequiredMixin, DeleteView):
    model           = Partido
    fields          = "__all__"
    template_name   = "torneos/ABM_partidos/partido_baja.html"
    success_url     = reverse_lazy('partidos')

    def get_success_url(self):
        print('get_success_url =======>>>>>>> ',self.kwargs)
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['torneo_id']})  


class ListaPartido(LoginRequiredMixin, ListView):
    model               = Torneo
    form_class          = ListaPartido_form
    context_object_name = "partidos"
    template_name       = "torneos/lista_partidos.html"

    def get_form_kwargs(self):
            kwargs = super(ListaPartido, self).get_form_kwargs()
            kwargs.update({
                'pk': self.kwargs['torneo_id'],
                })
            return kwargs
    
    def get_initial(self):
        initial = super(ListaPartido, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('torneo_id'),} )
        return initial
    
    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['torneo'] = self.kwargs.get('torneo_id')
        context['partidos'] = Partido.objects.filter(torneo=context['torneo'])
        #contex['tareas'] -> importante apuntar al context_object_name que se quiere
        #filter(tarea_usario=self.request.user) -> importante, seleccionar attributo a filtrar definido en models. para la clase en la que se esta trabajando
        #context['partidos'] = context['partidos'].filter(Partido_usario=self.request.user)
        #context['count'] = context['tareas'].filter(tarea_completada=False).count()

        #logica del buscardor
        search_input = self.request.GET.get('fecha') or ''
        if search_input:
            context['partidos'] = context['partidos'].filter(Partido_local__icontains=search_input)
        context['search_input'] = search_input
        return context    
     
class crea_Fixture(LoginRequiredMixin, DetailView):
    model               = Torneo
    form_class          = Fixture_form
    context_object_name = "fixture"
    template_name = "torneos/ABM_partidos/crear_fixtures.html"
    success_url     = reverse_lazy('torneo_home')

    def get_form_kwargs(self):
        print('get_form_kwargs ======>>>>>')    
        kwargs = super(crea_Fixture, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
            })
        return kwargs

    def get_initial(self):
        initial = super(crea_Fixture, self).get_initial()
        initial.update({ 'pk' : self.kwargs.get('pk'),} )
        return initial

    def get_context_data(self, **kwargs): #genera un filtro por usuario, para privacidad de datos
        context = super().get_context_data(**kwargs) 
        context['torneoID'] = self.kwargs.get('pk')
        torneo = Torneo.objects.filter(id=context['torneoID'])
        context['torneo'] = torneo
        return context 

    def get_success_url(self):
        print('get_success_url =======>>>>>>> ',self.kwargs)
        return reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['pk']})        

    def form_valid(self, form):
        return super(crea_Fixture, self).form_valid(form)
    
    def get(self, request, *args, **kwargs):    
        torneo = Torneo.objects.get(pk=self.kwargs.get('pk'))
        Alta_fixture(torneo)
        return HttpResponseRedirect (reverse_lazy('torneo_home', kwargs={'pk': self.kwargs['pk']})     )


def Alta_fixture(torneo):
    grupo = [] # lista de grupos, en cada grupo hay lista de equipos
    grupo_equipos = []
    x = 0

    #obtengo todos los equipo del grupo
    for tpogrupo in Grupo.objects.filter(toreno=torneo):    
        #partidos_grupo.append(Grupos[x][0])
        for clasificado in Clasificado.objects.filter(torneo=torneo).filter(grupo=tpogrupo):
            grupo_equipos.append(clasificado)               
        grupo.append(grupo_equipos)
        grupo_equipos = []
        x += 1
        #print('GRUPO =============>>>>>>>>>>', grupo)
    
    #creo partidos fase de grupos
    x = 0
    while x < len(grupo):
        contador =  1
        grupo_equipos = grupo[x].copy()
        grupo_equipos.pop(0)
        for clasificado in grupo[x]:
            for equipo in grupo_equipos:
                codigo  = clasificado.grupo.nombre + "_" + str(int(contador))
                if contador // 2:
                    local     = clasificado.equipo
                    visitante = equipo.equipo
                else:
                    local     = equipo.equipo
                    visitante = clasificado.equipo
                Partido.objects.create(torneo=torneo,codigo=codigo,local=local,visitante=visitante,resultado='P')    
                contador += 1
            grupo_equipos.pop(0) # por cada vuelta le saco 1 equipo a este grupo
            if not grupo_equipos:
                break
        x += 1        

    #Armo partidos playoff
    # identifico si hay playoff o no. 
    # Si hay tambien identifico cuantas llaves van a terner los playoff del torneo
    playoff = -1
    if torneo.clasificanXgrupo > 1:
        playoff = (torneo.clasificanXgrupo * torneo.grupos) / 2
    #cargo encuentros playoff, las llaves solamente van a tener el codigo partido
    # son teoricas, solo se sabe que grupo se cruza con quien.  
    x = 0
    g = 0
    llave_inicio = 0
    llave = []
    llave_partidos = []
    while playoff >=0:
        contador = 1
        if llave_inicio == 0: #genero la base de los playoff creando partidos y cargando array con los codigos de cada partido de la llave
            while g < len(grupo):  
                grupo1 = grupo[g][0]
                grupo2 = grupo[g+1][0]            
                codigo_new = str(int(playoff))+"_"+str(int(contador))+" 1"+ grupo1.grupo.nombre +" vs 2"+ grupo2.grupo.nombre
                Partido.objects.create(torneo=torneo, codigo=codigo_new ,resultado='P')
                llave_partidos.append(codigo_new)
                contador += 1
                codigo_new = str(int(playoff))+"_"+str(int(contador))+" 1"+ grupo2.grupo.nombre +" vs 2"+ grupo1.grupo.nombre
                Partido.objects.create(torneo=torneo, codigo=codigo_new ,resultado='P')
                llave_partidos.append(codigo_new)
                contador += 1
                g += 2
            llave.append(llave_partidos) 
            llave_partidos = []   
        else:
            llave_partidos = []
            g = 0
            inicio = llave[len(llave)-1]
            while g < len(inicio)-1:
                if len(llave) == 1 and playoff >2: #me aseguro que en despues de la primer etapa de playoff no se crucen los equipos del mismo grupo clasificatorio
                    grupo1 = inicio[g].split(" ")
                    grupo2 = inicio[g+2].split(" ")
                    codigo_new = str(int(playoff))+"_"+str(int(contador))+" "+grupo1[0]+' vs '+grupo2[0]
                    Partido.objects.create(torneo=torneo,codigo=codigo_new,resultado='P')
                    llave_partidos.append(codigo_new)
                    contador += 1
                    grupo1 = inicio[g+1].split(" ")
                    grupo2 = inicio[g+3].split(" ")                    
                    codigo_new = str(int(playoff))+"_"+str(int(contador))+" "+grupo1[0]+' vs '+grupo2[0]
                    Partido.objects.create(torneo=torneo,codigo=codigo_new,resultado='P')
                    llave_partidos.append(codigo_new)
                    contador += 1
                    g += 4
                    if g == len(inicio)-3:
                        g = len(inicio)
                else: 
                    grupo1 = inicio[g].split(" ")   
                    grupo2 = inicio[g+1].split(" ")
                    codigo_new = str(int(playoff))+"_"+str(int(contador))+" "+grupo1[0]+' vs '+grupo2[0]
                    Partido.objects.create(torneo=torneo,codigo=codigo_new,resultado='P')
                    llave_partidos.append(codigo_new)
                    if playoff == 1: #agrego la final ya que si dejo que llegue a cero en la siguente vuelta len(inicio) va a tener 1 y el while se rompe.
                        llave.append(llave_partidos) 
                        llave_partidos = []
                        grupo1 = inicio[g].split(" ")   
                        grupo2 = inicio[g+1].split(" ")
                        codigo_new = str(int(playoff-1))+"_"+str(int(contador))+" "+grupo1[0]+' vs '+grupo2[0]
                        Partido.objects.create(torneo=torneo,codigo=codigo_new,resultado='P')
                        llave_partidos.append(codigo_new)
                        llave.append(llave_partidos) 
                        g += 2  
                    g += 2                 
                    contador += 1
            if playoff > 1:        
                llave.append(llave_partidos) 
               
        if playoff > 1:  
            playoff = playoff / 2             
        else:
            playoff -= 1
        llave_inicio += 1    
                  
def actualiza_ranking(torneo):
    #desde el torneo, actualizo el ranking de los clasificados, si tienen partidos con resultado diferente a Pendiente.
    if torneo.fase == 'Grupos' or torneo.fase == 'Pendiente':
        for grupo in Grupo.objects.filter(toreno=torneo):            
            for clasificado in Clasificado.objects.filter(torneo=torneo).filter(grupo=grupo):        
                jugados     = 0
                puntos      = 0
                ganados     = 0
                empatados   = 0
                perdidos    = 0
                goles_F     = 0
                goles_C     = 0
                goles_D     = 0
                for partido in Partido.objects.filter(torneo=torneo).filter(local=clasificado.equipo).exclude(resultado='P'):
                    grupo_cod = partido.codigo.split("_",1)
                    if grupo_cod[0] == grupo.nombre:                        
                        jugados += 1
                        goles_F += partido.score_local
                        goles_C += partido.score_visitante
                        goles_D += partido.score_local - partido.score_visitante
                        if partido.resultado == 'L':
                            ganados += 1
                            puntos  += 3
                        if partido.resultado == 'E':
                            empatados += 1
                            puntos    += 1
                        if partido.resultado == 'V':
                            perdidos += 1

                for partido in Partido.objects.filter(torneo=torneo).filter(visitante=clasificado.equipo).exclude(resultado='P'):
                    grupo_cod = partido.codigo.split("_",1)
                    if grupo_cod[0] == grupo.nombre:
                        jugados += 1
                        goles_F += partido.score_visitante
                        goles_C += partido.score_local
                        goles_D += partido.score_visitante - partido.score_local 
                        if partido.resultado == 'V':
                            ganados += 1
                            puntos  += 3
                        if partido.resultado == 'E':
                            empatados += 1
                            puntos    += 1
                        if partido.resultado == 'L':
                            perdidos += 1      
                        
                clasificado.jugados     = jugados 
                clasificado.puntos      = puntos
                clasificado.ganados     = ganados
                clasificado.empatados   = empatados
                clasificado.perdidos    = perdidos
                clasificado.goles_F     = goles_F
                clasificado.goles_C     = goles_C
                clasificado.goles_D     = goles_D
                clasificado.activo = True
                clasificado.save()

