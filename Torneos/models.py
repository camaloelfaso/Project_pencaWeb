from django.contrib.auth.models import User
from email.policy import default
from threading import activeCount
from tkinter import Widget
from django.db import models
import datetime






# Create your models here.

PENDIENTE   = 'P'
EMPATE      = 'E'
LOCAL       = 'L'
VISITANTE   = 'V'
STATUS      = [
    (PENDIENTE, 'Pendiente'),
    (EMPATE, 'Empate'),
    (LOCAL, 'Local'),
    (VISITANTE, 'Visitante')
]  

PENDIENTE = 'Pendiente'     
GRUPOS    = 'Grupos'
OCTAVOS   = 'Octavos'
CUARTOS   = 'Cuartos'
SEMIS     = 'Semis'
TER_CUAR  = '3er y 4to'
FINAL     = 'Final' 
FASES     = [
    (PENDIENTE, 'Pendiente'),
    (GRUPOS, 'Grupos'),
    (OCTAVOS, 'Octavos'),
    (CUARTOS, 'Cuartos'),
    (SEMIS, 'Semis'),
    (TER_CUAR, '3er y 4to'),
    (FINAL, 'Final')   
]
IDA = 'I'
IDA_VUELTA = 'IV'
TPO_GRUPO = [
    (IDA, 'Ida'),
    (IDA_VUELTA, 'Ida y Vuelta'),    
]

class Equipo(models.Model):
    nombre       = models.CharField(max_length=50)
    ranking_fifa = models.IntegerField(default=0)
    bandera      = models.ImageField(upload_to='equipos_foto', null=True, blank=True)

    def __str__(self):
        return self.nombre + "- Ranking Fifa: " + str(self.ranking_fifa)

    class Meta:
        ordering = ['nombre']    

class Torneo(models.Model):
    nombre           = models.CharField(max_length=200)
    fecha            = models.DateTimeField(editable = True, null=True, blank=True)
    fase             = models.CharField(max_length=20, choices=FASES, default=PENDIENTE)
    cntequipos       = models.IntegerField(default=32)
    grupos           = models.IntegerField(default=8)
    grupos_mod       = models.CharField(max_length=2, choices=TPO_GRUPO, default=IDA)
    clasificanXgrupo = models.IntegerField(default=2)
    equipos          = models.ManyToManyField(Equipo,through='Clasificado')
    torneoPadre      = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='Torneo_padre')

    def __str__(self):
        texto = self.nombre + " - " + self.fase     
        return texto

class Grupo(models.Model):
    toreno = models.ForeignKey(Torneo,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        
        return self.nombre
    
    class Meta:
        ordering = ['nombre']

class Clasificado(models.Model):
    torneo      = models.ForeignKey(Torneo,on_delete=models.CASCADE)
    equipo      = models.ForeignKey(Equipo,on_delete=models.CASCADE)
    grupo       = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    activo      = models.BooleanField(default=False)
    puntos      = models.IntegerField(default=0) 
    jugados     = models.IntegerField(default=0) 
    ganados     = models.IntegerField(default=0)
    empatados   = models.IntegerField(default=0)
    perdidos    = models.IntegerField(default=0)
    goles_F     = models.IntegerField(default=0)
    goles_C     = models.IntegerField(default=0)
    goles_D     = models.IntegerField(default=0)


    def __str__(self):
        return self.equipo.nombre
    
    class Meta:
        ordering = ['grupo','-puntos','-goles_D']

class Partido(models.Model):
    torneo          = models.ForeignKey(Torneo, on_delete=models.CASCADE, null=False,blank=False)
    codigo          = models.CharField(max_length=30, default='')  
    fecha           = models.DateTimeField(editable = True, null=True, blank=True)
    local           = models.ForeignKey(Equipo, on_delete=models.CASCADE,  null=True, blank=True, related_name='Partido_local')
    visitante       = models.ForeignKey(Equipo, on_delete=models.CASCADE,  null=True, blank=True, related_name='Partido_visitante')
    score_local     = models.IntegerField(default=0)
    score_visitante = models.IntegerField(default=0)
    resultado       = models.CharField(max_length=1, choices=STATUS, default=EMPATE) 
    modif_ranking   = models.BooleanField(default=False)       
   
    class Meta:
        ordering = ['fecha', 'torneo']

   

    def __str__(self):
        opcion = self.codigo.split('_')
 #       if self.local.nombre and self.visitante.nombre:
 #           texto = self.local.nombre + " vs " + self.visitante.nombre
 #       elif self.local.nombre and  not self.visitante.nombre:
 #           texto = self.local.nombre + " vs " + opcion[2]
 #       elif not self.local.nombre and self.visitante.nombre:
 #           texto = opcion[1]  + " vs " + self.visitante.nombre    
 #       else:
        if len(opcion)>2:
            texto = opcion[1] + " vs " + opcion[2]
        elif len(opcion) == 2:
            texto = self.codigo 
        else:
            texto = ''

#        now   = datetime.datetime.now()
#        if self.fecha >= now : 
#            texto = self.local.nombre + " ( "+ str(self.score_local)  + " ) vs ( "+ str(self.score_visitante) +" ) "+  self.visitante.nombre    
        return texto

class Penca(models.Model):
    nombre          = models.CharField(max_length=200)
    fecha           = models.DateTimeField(editable = True, null=True, blank=True)
    torneo          = models.ForeignKey(Torneo,on_delete=models.CASCADE)
    #participantes   = models.ManyToManyField(User,through='Participante',related_name='Penca_participantes')
    administrador   = models.ForeignKey(User,on_delete=models.CASCADE, related_name='Penca_admin', null=True, blank=True)
    buy_in          = models.FloatField(default=0)
    pts_ganador     = models.IntegerField(default=3)
    pts_resultado   = models.IntegerField(default=2)
    pts_pasafase    = models.IntegerField(default=6)
    pts_terycuar    = models.IntegerField(default=6)
    pts_segundo     = models.IntegerField(default=10)
    pts_primero     = models.IntegerField(default=20)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['fecha','nombre','torneo']

class Participante(models.Model):
    penca           = models.ForeignKey(Penca,on_delete=models.CASCADE)             
    usuario         = models.ForeignKey(User,on_delete=models.CASCADE)
    torneo_hijo     = models.ForeignKey(Torneo,on_delete=models.CASCADE, null=True, blank=True)
    puntos          = models.IntegerField(default=0) 
    pts_ganador     = models.IntegerField(default=0)
    pts_resultado   = models.IntegerField(default=0)
    pts_pasafase    = models.IntegerField(default=0)
    pts_terycuar    = models.IntegerField(default=0)
    pts_segundo     = models.IntegerField(default=0)
    pts_primero     = models.IntegerField(default=0)


    def __str__(self):
        return self.usuario.first_name + " - " + self.penca.nombre
    class Meta:
        ordering = ['usuario','-puntos']