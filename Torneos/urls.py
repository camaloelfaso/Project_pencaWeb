from django.urls import path
from .views import * # AltaEquipo, CustomLoginView, AltaUsuario, ListaEquipos, UpdEquipo, DltEquipo, AltaClasificado, DltClasificado, UpdClasificado, ListaClasificado, HomeView, AltaTorneo, UpdTorneo, DltTorneo, ListaTorneo, TorneoDetalle
from .forms import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),    
    path('register/', AltaUsuario.as_view(), name='alta_usuario'),   

    path('<int:penca_id>/participante/nuevo/', AltaParticipante.as_view(), name="participante_alta"),
    path('<int:penca_id>/participante/upd/<int:pk>/', AltaParticipante.as_view(), name="participante_upd"),
    path('<int:penca_id>/participante/delete/<int:pk>/', DltParticipante.as_view(), name="participante_dlt"),
    
 
    path('penca-alta/', AltaPenca.as_view(), name="penca_alta"),
    path('penca-upd/<int:pk>', UpdPenca.as_view(), name="penca_upd"),
    path('penca-dlt/<int:pk>', DltPenca.as_view(), name="penca_dlt"),
    path('penca/<int:pk>/home', PencaHome.as_view(), name="penca_home"),
    path('penca/<int:pk>/config', PencaConfig.as_view(), name="penca_config"),

    path('equipo/', ListaEquipos.as_view(), name='equipos'),
    path('equipo-alta/', AltaEquipo.as_view(), name="equipo_alta"),
    path('equipo-upd/<int:pk>', UpdEquipo.as_view(), name="equipo_upd"),
    path('equipo-dlt/<int:pk>', DltEquipo.as_view(), name="equipo_dlt"),
    
    path('<int:torneo_id>/clasificado/', ListaClasificado.as_view(), name='clasificados'),
    path('<int:torneo_id>/clasificado/nuevo/', AltaClasificado.as_view(), name="clasificado_alta"),
    path('<int:torneo_id>/clasificado/upd/<int:pk>/', UpdClasificado.as_view(), name="clasificado_upd"),
    path('<int:torneo_id>/clasificado/delete/<int:pk>/', DltClasificado.as_view(), name="clasificado_dlt"),

    path('<int:torneo_id>/partido/', ListaPartido.as_view(), name='partidos'),
    path('<int:torneo_id>/partido/nuevo/', AltaPartido.as_view(), name="partido_alta"),
    path('<int:torneo_id>/partido/upd/<int:pk>', UpdPartido.as_view(), name="partido_upd"),
    path('<int:torneo_id>/partido/delete/<int:pk>', DltPartido.as_view(), name="partido_dlt"),    

    path('torneo/', ListaTorneo.as_view(), name='torneos'),
    path('torneo/nuevo', AltaTorneo_view, name="torneo_alta"),
    path('torneo/upd/<int:pk>', UpdTorneo.as_view(), name="torneo_upd"),
    path('torneo/<int:pk>/home', TorneoDetalle.as_view(), name='torneo_home'),
    path('torneo/delete/<int:pk>', DltTorneo.as_view(), name="torneo_dlt"),

    path('torneo/<int:pk>/fixture/', crea_Fixture.as_view(), name="genera_fixture"),
    path('torneo/<int:pk>/cargaClasificados/', crea_Clasificados.as_view(), name="carga_clasificados"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
