from cart.serializers import CartSerializers,AddCartSerializers,CartProduct
from cart.models import Cart
from shop.models import Shop
from product.models import Product
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_api.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema



class CartList(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
 
    def get(self, request, shop_uid, format=None):
        merchant = request.user
        try:
            shop = Shop.objects.get(uid=shop_uid)
        except Shop.DoesNotExist:
            return Response({'message': 'Shop Not Found with this shop uid'}, status=status.HTTP_400_BAD_REQUEST)
        
        if shop.merchant == merchant:
            cart_items = Cart.objects.filter(shop__uid=shop_uid)
            if cart_items:      
                serializer = CartSerializers(cart_items, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No item found in your cart.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'message': 'You are not proper merchant to view this cart'}, status=status.HTTP_404_NOT_FOUND)
    
    @extend_schema(
    request=CartProduct,
    responses={201: CartProduct},
    )
    def post(self, request, shop_uid, format=None):
        merchant = request.user
        try:
            shop = Shop.objects.get(uid=shop_uid)
        except Shop.DoesNotExist:
            return Response({'message': 'Shop Not Found with this shop uid'}, status=status.HTTP_400_BAD_REQUEST)
        
        if shop.merchant == merchant:
            if shop.is_active:
                try:
                    product = Product.objects.get(uid=request.data.get('product'))
                except Product.DoesNotExist:
                    return Response({'message': 'product not found with this uid'}, status=status.HTTP_400_BAD_REQUEST)
                
                data={
                    'shop':shop.id,
                    'product':product.id,
                    'quantity':1
                }

                serializer = AddCartSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Cart added sucessfully'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Your shop is not active yet'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message': 'You are not proper merchant to add cart'}, status=status.HTTP_404_NOT_FOUND)