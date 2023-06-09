from shop.serializers import ShopSerializers,ShopPostSerializers,ActiveShopSerializer
from shop.models import Shop
from category.models import Category
from account_api.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_api.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.http import Http404
from drf_spectacular.utils import extend_schema


class ShopListView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shops = Shop.objects.all()
        if shops:
            serializer = ShopSerializers(shops, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response({'message': 'No shop found '}, status=status.HTTP_404_NOT_FOUND)


# shop view for merchant 

class ShopAPIView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        merchant = request.user  # logged-in merchant is stored in the request
        shops = Shop.objects.filter(merchant=merchant)

        if shops:
            serializer = ShopSerializers(shops, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No shop found for this merchant.'}, status=status.HTTP_404_NOT_FOUND)
              
    @extend_schema(
    request=ShopPostSerializers,
    responses={201: ShopPostSerializers},
    )
    def post(self, request):
        merchant_uid = request.data.get('merchant')
        category_uid = request.data.get('category')

        # # first find merchant and category exits with their uid
        try:
            merchant = User.objects.get(uid=merchant_uid)
            category = Category.objects.get(uid=category_uid)
        except User.DoesNotExist:
            return Response({'message': 'Merchant not found with this uid'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found with this uid'}, status=status.HTTP_400_BAD_REQUEST)
        data={
            'merchant':merchant.id,
            'shop_name':request.data.get('shop_name'),
            'category':category.id,
            'description':request.data.get('description'),
            'active_code':request.data.get('active_code'),
            }
        serializer = ShopPostSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Shop added sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopDetailView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get_object(self, uid):
        try:
            return Shop.objects.get(uid=uid)
        except Shop.DoesNotExist:
            raise Http404

    def get(self, request, uid, format=None):
        shop = self.get_object(uid)
        if shop.merchant.uid != request.user.uid:
            return Response({'message': 'You are not authorized to view this shop'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ShopSerializers(shop)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @extend_schema(
    request=ShopPostSerializers,
    responses={201: ShopPostSerializers},
    )
    def put(self, request,uid, format=None):
        shop = self.get_object(uid)
        merchant_uid = request.data.get('merchant')
        category_uid = request.data.get('category')

        # # first find merchant and category exits with their uid
        try:
            merchant = User.objects.get(uid=merchant_uid)
            category = Category.objects.get(uid=category_uid)
        except User.DoesNotExist:
            return Response({'message': 'Merchant not found with this uid'}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found with this uid'}, status=status.HTTP_400_BAD_REQUEST)
        data={
            'merchant':merchant.id,
            'shop_name':request.data.get('shop_name'),
            'category':category.id,
            'description':request.data.get('description'),
            'active_code':request.data.get('active_code'),
            }
        serializer = ShopPostSerializers(shop, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Shop Updated Sucessfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,uid, format=None):
        shop = self.get_object(uid)
        shop.delete()
        return Response({"msg":"Shop Successfully Removed"},status=status.HTTP_204_NO_CONTENT)
    

# class ActiveShopView(APIView):
#     renderer_classes = [UserRenderers]
#     permission_classes = [IsAuthenticated]
#     @extend_schema(
#     request=ActiveShopSerializer,
#     responses={201: ActiveShopSerializer},
#     )
#     def post(self, request, shop_uid):
#         # Check if the merchant has any active shop already
#         if Shop.objects.filter(merchant=request.user, is_active=True).exists():
#             return Response({"msg": "You already have an active shop. Please log out from that shop."}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             shop = Shop.objects.get(uid=shop_uid)
#         except Shop.DoesNotExist:
#             return Response({'message': 'Shop not found '}, status=status.HTTP_400_BAD_REQUEST)
       
#         serializer = ActiveShopSerializer(data=request.data)
        
#         if serializer.is_valid():
#             if shop.active_code == serializer.validated_data['active_code']:
#                 shop.is_active = True
#                 shop.save()
#                 return Response({"msg": "Shop Successfully Activated"}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"msg": "Code not match"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# class DeactiveShopView(APIView):
#     renderer_classes = [UserRenderers]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, shop_uid):
#         try:
#             shop = Shop.objects.get(uid=shop_uid)
#             shop.is_active = False
#             shop.save()
#             return Response({"msg": "Shop Successfully Deactivated"}, status=status.HTTP_201_CREATED)
#         except Shop.DoesNotExist:
#             return Response({'message': 'Shop not found '}, status=status.HTTP_400_BAD_REQUEST)
       
class ShopStatusView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ActiveShopSerializer,
        responses={201: ActiveShopSerializer},
    )
    def post(self, request, shop_uid, status):
        try:
            shop = Shop.objects.get(uid=shop_uid)
        except Shop.DoesNotExist:
            return Response({'message': 'Shop not found '}, status=status.HTTP_400_BAD_REQUEST)

        if status == 'activate':
            return self.activate_shop(request, shop)
        elif status == 'deactivate':
            return self.deactivate_shop(request, shop)
        else:
            return Response({'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    def activate_shop(self, request, shop):
        if Shop.objects.filter(merchant=request.user, is_active=True).exists():
                return Response({"msg": "You already have an active shop. Please log out from that shop."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ActiveShopSerializer(data=request.data)

        if serializer.is_valid():
            if shop.active_code == serializer.validated_data['active_code']:
                shop.is_active = True
                shop.save()
                return Response({"msg": "Shop Successfully Activated"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "Code does not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def deactivate_shop(self, request, shop):
        shop.is_active = False
        shop.save()
        return Response({"msg": "Shop Successfully Deactivated"}, status=status.HTTP_201_CREATED)

