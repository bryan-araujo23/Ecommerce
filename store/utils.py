# armazenar algumas funções auxiliares que iremos criar.

# O formato JSON é utilizado para estruturar dados em formato de texto
# e permitir a troca de dados entre aplicações de forma simples, leve e rápida.
# Por isso é tão importante saber como é estruturado e as principais diferenças com o modelo XML.

import json
from .models import  *


def cookieCart(request):
    # Cria um carrinho vazio por enquanto para usuários não autenticados
    try:
        cart = json.loads(request.COOKIES['cart'])  # Tenta carregar o carrinho a partir dos cookies.
    except:
        cart = {}  # Se falhar, cria um carrinho vazio.
        print('CART:', cart)  # Imprime o carrinho (útil para debug).

    items = []  # Lista para armazenar os itens do carrinho.
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}  # Dicionário para armazenar informações do pedido.
    cartItems = order['get_cart_items']  # Inicializa a quantidade total de itens no carrinho.

    for i in cart:
        # Usamos o bloco try para evitar erros causados por itens que podem ter sido removidos do banco de dados.
        try:
            cartItems += cart[i]['quantity']  # Atualiza a quantidade total de itens no carrinho.

            product = Product.objects.get(id=i)  # Obtém o produto associado ao ID no carrinho.
            total = (product.price * cart[i]['quantity'])  # Calcula o total para esse item no carrinho.

            order['get_cart_total'] += total  # Atualiza o total do carrinho.
            order['get_cart_items'] += cart[i]['quantity']  # Atualiza a quantidade total de itens no carrinho.

            item = {
                'id': product.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'digital': product.digital,
                'get_total': total,
            }
            items.append(item)  # Adiciona o item à lista de itens do carrinho.

            if product.digital == False:
                order['shipping'] = True  # Se o produto não for digital, define a necessidade de envio.

        except:
            pass  # Ignora erros e continua para o próximo item do carrinho.

    return {'cartItems': cartItems, 'order': order, 'items': items}  # Retorna um dicionário com as informações do carrinho.


def cartData(request):
	if request.user.is_authenticated:      # Verifica se o usuário está autenticado.
		customer = request.user.customer   # Obtém o cliente associado ao usuário autenticado.
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# Obtém o pedido do cliente ou cria um novo se não existir um pedido não concluído.
		items = order.orderitem_set.all()  # Obtém todos os itens do pedido associado ao cliente.
		cartItems = order.get_cart_items   # Obtém a quantidade total de itens no carrinho do pedido
	else:                                  # Crie um carrinho vazio por enquanto para usuário não logado
		cookieData = cookieCart(request)   # Obtém dados do carrinho a partir de cookies.
		cartItems = cookieData['cartItems'] # Obtém a quantidade total de itens no carrinho a partir dos cookies.
		order = cookieData['order']         # Obtém o pedido a partir dos cookies.
		items = cookieData['items']         # Obtém os itens do carrinho a partir dos cookies.

	return {'cartItems': cartItems, 'order': order, 'items': items}