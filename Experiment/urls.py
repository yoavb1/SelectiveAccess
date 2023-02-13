from . import views
from django.urls import path

app_name = "experiment"

urlpatterns = [
    path('', views.registration, name='registration'),
    path('registration/', views.registration, name='registration'),
    path('consent_form/', views.consent_form, name='consent_form'),
    path('end/', views.end, name='end'),
    path('instructions/', views.instructions, name='instructions'),
    path('game/', views.game, name='game'),
    path('server/', views.server, name='server'),
    path('parameters/', views.parameters, name='parameters'),
    path('progress/', views.progress, name='progress'),
    path('nasa_tlx/', views.nasa_tlx, name='nasa_tlx'),
    path('trust/', views.trust, name='trust'),
    path('warning/', views.warning, name='warning'),
    path('completed/', views.completed, name='completed'),

]