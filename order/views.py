from order.serializers import OrderSerializers,OrderItemSerializers
from order.models import Order,OrderItem
from shop.models import Shop
from cart.models import Cart,CartItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_api.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.http import Http404
import json



# class OrderApiView(APIView):
#     renderer_classes = [UserRenderers]
#     permission_classes = [IsAuthenticated]

#     def get(self,request,shop_uid):

#         try:
#             shop = Shop.objects.get(uid=shop_uid)
#         except Shop.DoesNotExist:
#             return Response({'message': 'Shop not found with this shop uid'}, status=status.HTTP_404_NOT_FOUND)
        
#         # check merchant is shop merchant
#         if shop.merchant == request.user:
#             # find orders
#             orders = Order.objects.filter(shop=shop)

#             if orders :
#                 serializer = OrderSerializers(orders,many=True)
#                 return Response(serializer.data,status=status.HTTP_200_OK)
#             else:
#                 return Response({'message': 'No order found for this shop.'}, status=status.HTTP_404_NOT_FOUND)
            
#         return Response({'message':'you are not merchant of this shop'},status=status.HTTP_403_FORBIDDEN)


#     def post(self,request,shop_uid):

#         try:
#             shop = Shop.objects.get(uid=shop_uid)
#         except Shop.DoesNotExist:
#             return Response({'message': 'Shop not found with this shop uid'}, status=status.HTTP_404_NOT_FOUND)
        
#         if shop.is_active:
            
#             cart_items = Cart.objects.filter(shop=shop)

#             if cart_items:
#                 product = []
#                 total_price = 0
#                 for item in cart_items:
#                     product_data = {   
#                         'name': item.product.product_name,
#                         'quantity': item.quantity
#                     }
#                     product.append(product_data)
#                     product_price = item.product.price * item.quantity
#                     total_price += product_price 

#                 # Convert product to JSON
#                 product_json = json.dumps(product)
                
#                 data = {
#                     'shop':shop.id,
#                     'product':product_json,
#                     'total_price':total_price
#                 }
#                 serializer = OrderPostSerializers(data=data)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save()
#                     # Delete cart items
#                     cart_items.delete()
#                     return Response({'message':'Order Placed Successfully'},status=status.HTTP_201_CREATED)
                
#             return Response({'message': 'No product found in cart'}, status=status.HTTP_404_NOT_FOUND)
        
#         return Response({'message': 'Your shop is not active yet'}, status=status.HTTP_404_NOT_FOUND)



class OrderApiView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self,request,uid):
        try:
            shop = Shop.objects.get(uid=uid)
        except Shop.DoesNotExist:
            return Response({'message': 'Shop not found with this shop uid'}, status=status.HTTP_404_NOT_FOUND)
        
        # find orders
        orders = Order.objects.filter(organization=shop)

        if orders :
            order_data = []
            for order in orders:
                order_items = OrderItem.objects.filter(order=order)
                serializer = OrderSerializers(order)
                order_data.append({
                    'order': serializer.data,
                    'order_items': OrderItemSerializers(order_items, many=True).data
                })
            return Response(order_data,status=status.HTTP_200_OK)
    
        return Response({'message': 'No order found for this shop.'}, status=status.HTTP_404_NOT_FOUND)


    def post(self,request,uid):
        try:
            shop = Shop.objects.get(uid=uid)
        except Shop.DoesNotExist:
            return Response({'message': 'Shop not found with this shop uid'}, status=status.HTTP_404_NOT_FOUND)
        
        if shop.is_active:
            
            cart_items = CartItem.objects.filter(cart__organization=shop)

            if cart_items:
                order = Order.objects.create(organization=shop,order_status='PENDING',total_price=0)
                total_price = 0
                # create order item 
                for item in cart_items:
                    OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.price)
                    item_price = item.price*item.quantity
                    total_price += item_price

                order.total_price=total_price
                order.save()

                # Now Delete cart items
                cart_items.delete()

                return Response({'message': 'Order Placed Successfully'}, status=status.HTTP_201_CREATED)
            
            return Response({'message': 'You dont have any item to order'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message': 'Your shop is not active yet'}, status=status.HTTP_404_NOT_FOUND)