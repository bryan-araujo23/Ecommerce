from django.shortcuts import render
from django.http import JsonResponse  # é parte do módulo django.http para retornar respostas HTTP no formato JSON
import json  # módulo json que permite funçãoes para trabalhar com dados json  como serialização e desserialização.
import datetime
from .models import *


def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)


def cart(request):

	if request.user.is_authenticated:           # Se usuário estiver autenticado
		customer = request.user.customer        # cliente = solicita usuário cliente
		order, created = Order.objects.get_or_create(customer=customer, complete=False)    # encontre ou crie e faça o pedido usando o método get_or_create().
		items = order.orderitem_set.all()       # consultar os itens do carrinho com order.orderitem_set.all() 
	else: # Se o usuário não estiver autenticado/logado, queremos retornar uma lista vazia chamada itens.
		items = [] 
		order = {'get_cart_total':0, 'get_cart_items':0}
		
	context = {'items':items, 'order': order}
	return render(request, 'store/cart.html', context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		#Se o usuário não estiver autenticado/logado, queremos retornar uma lista vazia chamada itens.
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
	return render(request, 'store/checkout.html', context)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order = transaction_id = transaction_id
	else:
		print('User is not logged in')
	return JsonResponse()

	return JsonResponse('Payment subbmitted..', safe=False)

def updateItem(request):
	return JsonResponse('Item was added', safe=False)