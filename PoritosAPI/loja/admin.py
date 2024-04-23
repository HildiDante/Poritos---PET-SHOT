from django.contrib import admin

from loja.models import Produto
from loja.models import Compra

admin.site.register(Produto)
admin.site.register(Compra)
