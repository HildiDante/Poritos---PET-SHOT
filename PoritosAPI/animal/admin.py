from django.contrib import admin

from animal.models.animal import Animal
from animal.models.reserva import Reserva
from animal.models.servico import Servico

admin.site.register(Animal)
admin.site.register(Servico)
admin.site.register(Reserva)