from ast import Eq
from dataclasses import fields
from datetime import datetime
from email.policy import default
from pyexpat import model
import string
from tkinter import DISABLED
from tkinter.ttk import Widget
from xmlrpc.client import FastParser
from django import forms
from django.forms import ModelForm, DateField
from django.utils import timezone

from .models import Equipo, Grupo, Participante, Partido, Penca, Torneo, Clasificado, User
from django.urls import reverse_lazy
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField



############################################################## WIDGET
class NoInput(forms.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(value)

class StaticField(forms.Field):
    
    widget = NoInput
    
    def clean(self, value):
        return 

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            img_html = mark_safe(
                f'<br><br><img src="{value.url}" width="50" />')
            return f'{input_html}{img_html}'
        return input_html

class LastActiveForm(forms.Form):
    """
    Last Active Date Form
    """
    last_active = forms.DateField(widget=DateTimeInput) 

class Penca_form(ModelForm):
    class Meta:
        model  = Penca
        fields = '__all__'
        widgets={'fecha':DateTimeInput()}   

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM

        varibale = kwargs.pop('initial')

        administrador = User.objects.get(id=varibale['pk'])
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(Penca_form, self).__init__(*args, **kwargs)    
        self.fields['administrador'].initial = administrador  
        self.fields['torneo'].queryset       = Torneo.objects.filter(torneoPadre=None)    

class PencaUpd_form(ModelForm):
    class Meta:
        model  = Penca
        fields = '__all__'
        widgets={'fecha':DateTimeInput()}   

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(PencaUpd_form, self).__init__(*args, **kwargs)          


class PencaConfig_form(ModelForm):
    class Meta:
        model  = Penca
        fields = '__all__'
        #widgets={'fecha':DateTimeInput()}   

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        varibale = kwargs.pop('initial')

        penca = Penca.objects.get(id=varibale['pk'])
        print('penca ==>>>',penca)
        super(PencaUpd_form, self).__init__(*args, **kwargs)  
        self.fields['penca'].widget.attrs['disabled']           = 'disabled'        
        self.fields['torneo'].widget.attrs['disabled']          = 'disabled'
        self.fields['nombre'].widget.attrs['disabled']          = 'disabled'
        self.fields['fecha'].widget.attrs['disabled']           = 'disabled'
        self.fields['administrador'].widget.attrs['disabled']   = 'disabled'
        self.fields['buy_in'].widget.attrs['disabled']          = 'disabled'
        self.fields['pts_ganador'].widget.attrs['disabled']     = 'disabled'
        self.fields['pts_pasafase'].widget.attrs['disabled']    = 'disabled'
        self.fields['pts_terycuar'].widget.attrs['disabled']    = 'disabled'
        self.fields['pts_segundo'].widget.attrs['disabled']     = 'disabled'
        self.fields['pts_primero'].widget.attrs['disabled']     = 'disabled'

class ParticipanteAlta_form(ModelForm):
    class Meta:
        model  = Participante
        fields = '__all__'

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM

        varibale = kwargs.pop('initial')

        penca = Penca.objects.get(id=varibale['pk'])
        #torneo_hijo = Torneo.objects.update_or_create(nombre=penca.torneo.nombre,fecha=penca.torneo.fecha,fase=penca.torneo.fase,cntequipos=penca.torneo.cntequipos,grupos=penca.torneo.grupos,grupos_mod=penca.torneo.grupos_mod,clasificanXgrupo=penca.torneo.clasificanXgrupo,torneoPadre=penca.torneo)

        print('penca ===>>>',penca)
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(ParticipanteAlta_form, self).__init__(*args, **kwargs)    
        self.fields['penca'].initial = penca

        self.fields['torneo_hijo'].queryset = Torneo.objects.filter(id=penca.torneo.pk)

class ParticipanteUpd_form(ModelForm):
    class Meta:
        model  = Participante
        fields = '__all__'
    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM

        varibale = kwargs.pop('initial')

        penca = Penca.objects.get(id=varibale['pk'])

        print('penca ===>>>',penca)
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(ParticipanteUpd_form, self).__init__(*args, **kwargs)    
        self.fields['penca'].initial = penca  

class Equipo_form(ModelForm):

    def clean_due_back(self):
       data = self.cleaned_data['bandera']
       return data
    class Meta:
        model = Equipo
        fields = '__all__'
        widgets={'bandera':ImagePreviewWidget}

class Partido_Form(ModelForm):

    class Meta:
        model  = Partido
        fields = ['torneo', 'fecha', 'local', 'visitante', 'score_local', 'score_visitante']
        widgets={'fecha':DateTimeInput()}
        
    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        torneo = Torneo.objects.get(id=kwargs.pop('pk')) 
        
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(Partido_Form, self).__init__(*args, **kwargs)  
        equipos = filtraEquipo(torneo,'partido')
        #filtraEqupo trae los equipos disponibles para clasificar al torneo
        self.fields['torneo'].initial = torneo 
        #carga toreo que viene por url 
        #self.fields['torneo'].widget.attrs['disabled'] = 'disabled'
        #hace que el field no se puedea modificar
        self.fields['torneo'].queryset      = Torneo.objects.filter(id=torneo.pk) 
        self.fields['local'].queryset       = Equipo.objects.filter(id__in=equipos)
        self.fields['visitante'].queryset   = Equipo.objects.filter(id__in=equipos)
        
        #queryset le indica que tiene que ejecutrar el filtro que se asigna

class PartidoUpd_Form(ModelForm):

    class Meta:
        model  = Partido
        fields = ['torneo','fecha', 'local', 'visitante', 'score_local', 'score_visitante', 'resultado']
        widgets={'fecha':DateTimeInput()}
        


class Clasificado_form(forms.ModelForm):
    class Meta:
        model  = Clasificado
        fields = '__all__'

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
       # print('kwargs ======>>>>>', kwargs)
       # print('kwargs ======>>>>>', kwargs.get('initial'))
        varibale = kwargs.pop('initial')
       # print('kwargs ======>>>>>', varibale['pk'])
        torneo = Torneo.objects.get(id=varibale['pk']) 
        #torneo = Torneo.objects.get(id=kwargs.pop('pk')) 
                            
                        
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(Clasificado_form, self).__init__(*args, **kwargs)  
        equipos = filtraEquipo(torneo, 'clasificado')
        #filtraEqupo trae los equipos disponibles para clasificar al torneo
        self.fields['torneo'].initial = torneo 
        

        #carga toreo que viene por url 
        # self.fields['torneo'].widget.attrs['disabled'] = 'disabled'
        #hace que el field no se puedea modificar

        self.fields['equipo'].queryset = Equipo.objects.filter(id__in=equipos)
        self.fields['grupo'].queryset = Grupo.objects.filter(toreno=torneo) 
        #queryset le indica que tiene que ejecutrar el filtro que se asigna




def filtraEquipo(torneo, criterio):
    clasificados = Clasificado.objects.filter(torneo=torneo)
    equipos = []
    if criterio == 'clasificado':
        for equipo in Equipo.objects.all():
            esta = False
            for clasificado in clasificados:
                if equipo == clasificado.equipo:
                    esta =True
                    break
            if not esta:    
                equipos.append(equipo.pk)  
    if criterio == 'partido':
        for equipo in Equipo.objects.all():
            esta = False
            for clasificado in clasificados:
                if equipo == clasificado.equipo:
                    esta =True
                    break
            if esta:    
                equipos.append(equipo.pk)

    return equipos
    


class ClasificadoUPD_form(forms.ModelForm):
    class Meta:
        model  = Clasificado
        fields = '__all__'
    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super        
        super(ClasificadoUPD_form, self).__init__(*args, **kwargs)  


class Torneo_Form(ModelForm):
    class Meta:
        model   = Torneo
        fields  = '__all__'
        exclude = ['equipos']
        widgets ={'fecha':DateTimeInput()}

class ListaPartido_form(forms.ModelForm):
    class Meta:
        model  = Torneo
        fields = '__all__'
        widgets={'fecha':DateTimeInput()}
        
    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        #print('kwargs ======>>>>>', kwargs)
        #print('kwargs ======>>>>>', kwargs.get('initial'))
        varibale = kwargs.pop('initial')
        #print('kwargs ======>>>>>', varibale['pk'])
        torneo = Torneo.objects.get(id=varibale['pk']) 
        #torneo = Torneo.objects.get(id=kwargs.pop('pk'))   
        super(ListaPartido_form, self).__init__(*args, **kwargs)    


class Fixture_form(ModelForm):
    class Meta:
        model = Torneo
        fields = '__all__'

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        #print('kwargs ======>>>>>', kwargs)
        #print('kwargs ======>>>>>', kwargs.get('initial'))
        varibale = kwargs.pop('initial')
        #print('kwargs ======>>>>>', varibale['pk'])
        torneo = Torneo.objects.get(id=varibale['pk']) 
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(Fixture_form, self).__init__(*args, **kwargs)  

