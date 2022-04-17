import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from bake_end.models import Client, CartItem
from bake_end.tools import queryset_to_list


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCart(View):

    def patch(self, request, item_id):
        data = json.loads(request.body.decode("utf-8"))
        item = CartItem.objects.get(id=item_id)
        item.product_quantity = data['product_quantity']
        item.save()

        data = {
            'message': f'Item {item_id} has been updated'
        }

        return JsonResponse(data)

    def delete(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()

        data = {
            'message': f'Item {item_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartUpdate(View):

    def patch(self, request, item_id):
        data = json.loads(request.body.decode("utf-8"))
        item = CartItem.objects.get(id=item_id)
        item.product_quantity = data['product_quantity']
        item.save()

        data = {
            'message': f'Item {item_id} has been updated'
        }

        return JsonResponse(data)

    def delete(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()

        data = {
            'message': f'Item {item_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class Categories(View):
    def get(self, request):
        return JsonResponse(queryset_to_list(Client.objects.values()), status=201, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Products(View):
    def get(self, request):
        return JsonResponse(queryset_to_list(Client.objects.values()), status=201, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Clients(View):
    def get(self, request):
        return JsonResponse(queryset_to_list(Client.objects.values()), status=201, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ClientUpdate(View):

    def get(self, request, pk):
        return JsonResponse({'client': model_to_dict(Client.objects.get(id=pk))}, status=201, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        p_name = data.get('product_name')
        p_price = data.get('product_price')
        p_quantity = data.get('product_quantity')

        product_data = {
            'product_name': p_name,
            'product_price': p_price,
            'product_quantity': p_quantity,
        }

        client = Client.objects.create(**product_data)

        data = {
            "message": f"New item added to Cart with id: {client.id}"
        }
        return JsonResponse(data, status=201, safe=False)

    def patch(self, request, item_id):
        data = json.loads(request.body.decode("utf-8"))
        item = Clients.objects.get(id=item_id)
        item.product_quantity = data['product_quantity']
        item.save()

        data = {
            'message': f'Item {item_id} has been updated'
        }

        return JsonResponse(data)

    def delete(self, request, item_id):
        item = Clients.objects.get(id=item_id)
        item.delete()

        data = {
            'message': f'Item {item_id} has been deleted'
        }

        return JsonResponse(data)
