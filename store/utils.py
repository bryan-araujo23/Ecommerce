# armazenar algumas funções auxiliares que iremos criar.

# O formato JSON é utilizado para estruturar dados em formato de texto
# e permitir a troca de dados entre aplicações de forma simples, leve e rápida.
# Por isso é tão importante saber como é estruturado e as principais diferenças com o modelo XML.

import json
from .models import *


def cookieCart(request):
    return {}