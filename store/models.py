from django.db import models

from django.contrib.auth.models import User     # Modelo de Usuário padrão Django 


class Customer(models.Model):#Cliente
    """
    Junto com um modelo de Usuário, cada cliente conterá 
    um modelo de Cliente que mantém um relacionamento
    individual com cada usuário. (OneToOneField). 
    """
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # User Uma instância deste modelo será criada para cada cliente que se cadastrar em nosso site
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


 # @ property - transformar um método de uma classe em uma propriedade,
 # permitindo que você acesse esse método como se fosse um atributo.
 # Isso significa que você pode chamar o método sem usar parênteses. 

class Product(models.Model):#Produto
    """
    O modelo do produto representa os produtos que temos em loja.
    """
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True) # Se o produto é digital ou fisíco
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property 
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):#Ordem(um pedido será o resumo do pedido dos itens. Carrinho)

    """
    O modelo de pedido representará uma transação realizada ou pendente.
    O modelo conterá informações como ID da transação, dados concluídos
    e status do pedido. Este modelo será filho ou modelo do cliente, mas pai dos itens do pedido.
    """

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True) # data do pedido
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self): # Self é uma istância de Order
        return str(self.id)
    

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems]) # item contexto func cart, e do template cart
        return total


    @property
    def get_cart_total(self):

        """
            Definimos um relacionamento entre modelos(Order e OrderItem) 
            através de um fk, O DJANGO automaticamente cria um ATRIBUTO
            no modelo relacionado usando o nome do modelo em minúsculas seguido de "_set".
        """        
        orderitems = self.orderitem_set.all() # VAR(carrinho) = Order.OrdemItem.todos()
        total = sum([item.get_total for item in orderitems]) # item é contexto iterado em cart.html. get_total é uma func de OrderItem
        return total


class OrderItem(models.Model):#  itens no carrinho
    """
    Este modelo precisará de um atributo de produto conectado 
    ao modelo do produto, o pedido ao qual este item está conectado,
    a quantidade e a data em que este item foi adicionado ao carrinho.
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):#Endereço para envio
    """
    Este modelo será filho do pedido(Order) e só será criado se pelo menos 
    um item do pedido dentro de um pedido for um produto físico 
    (If Product.digital == False).
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) # relação com a tabela Customer
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address