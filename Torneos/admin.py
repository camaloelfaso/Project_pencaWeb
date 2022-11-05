from django.contrib import admin
from .models import *
# Register your models here.
class PartidoArmin(admin.ModelAdmin):
    list_display = ('torneo', 'codigo')
class EquipoArmin(admin.ModelAdmin):
    list_display = ('nombre','bandera')
class TorneoArmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha')    


admin.site.register(Partido, PartidoArmin)
admin.site.register(Equipo, EquipoArmin)

admin.site.register(Torneo, TorneoArmin)
admin.site.register(Clasificado)
admin.site.register(Grupo)
admin.site.register(Penca)
admin.site.register(Participante)
