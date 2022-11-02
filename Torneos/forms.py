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

from .models import Equipo, Grupo, Partido, Torneo, Clasificado
from django.urls import reverse_lazy
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField



############################################################## WIDGET

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
        fields = '__all__'
        widgets={'fecha':DateTimeInput()}

    def __init__(self, *args, **kwargs): #permite jugar con los valoer iniciales del FORM
        torneo = Torneo.objects.get(id=kwargs.pop('pk')) 
        
        #super() carga el form con los valores por defecto. por eso torneo se carga antes de llamar a super
        super(Partido_Form, self).__init__(*args, **kwargs)  
        equipos = filtraEquipo(torneo,'partido')
        #filtraEqupo trae los equipos disponibles para clasificar al torneo
        self.fields['torneo'].initial = torneo 
        #carga toreo que viene por url 
       # self.fields['torneo'].widget.attrs['disabled'] = 'disabled'
        #hace que el field no se puedea modificar

        self.fields['local'].queryset = Equipo.objects.filter(id__in=equipos)
        self.fields['visitante'].queryset = Equipo.objects.filter(id__in=equipos)
        
        #queryset le indica que tiene que ejecutrar el filtro que se asigna

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

