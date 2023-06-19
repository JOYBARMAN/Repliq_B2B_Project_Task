from product.serializers import ProductSerializers,ProductPostSerializers
from product.models import Product
from shop.models import Shop
from connection.models import Connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_api.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.http import Http404
from drf_spectacular.utils import extend_schema



class ProductAPIView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request ,uid):
        '''Get product list of merchant organization'''
        shop = Shop.objects.get(uid=uid)
        shop_products = Product.objects.filter(organization=shop)

        if shop.merchant.uid == request.user.uid:
            if shop_products:
                serializer = ProductSerializers(shop_products, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No product found for this organization.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'message': 'You are not merchant of this organization'}, status=status.HTTP_403_FORBIDDEN) 
        
    @extend_schema(
        request=ProductPostSerializers,
        responses={201: ProductPostSerializers},
    )
    def post(self, request,uid):
        '''Add product of merchant organization'''
        shop = Shop.objects.get(uid=uid)
        if shop.merchant.uid == request.user.uid:
            data={
                'organization':shop.id,
                'product_name':request.data.get('product_name'),
                'price':request.data.get('price'),
                'description':request.data.get('description'),
                'image':request.data.get('image'),
                }
            serializer = ProductPostSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product added sucessfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'You are not merchant of this organization'}, status=status.HTTP_403_FORBIDDEN)


class ProductDetailView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get_object(self, uid):
        try:
            return Product.objects.get(uid=uid)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request,org_uid,uid, format=None):
        '''Get product detail'''
        product = self.get_object(uid)
        if product.organization.merchant.uid != request.user.uid:
            return Response({'message': 'You are not authorized to view this product'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializers(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request,org_uid, uid, format=None):
        '''Update product informations'''
        product = self.get_object(uid)
        shop = Shop.objects.get(uid=org_uid)
        if shop.merchant.uid == request.user.uid:
            data={
                'organization':shop.id,
                'product_name':request.data.get('product_name'),
                'price':request.data.get('price'),
                'description':request.data.get('description'),
                'image':request.data.get('image'),
                }
            serializer = ProductPostSerializers(product,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product Updated sucessfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'You are not merchant of this shop'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request,uid,org_uid, format=None):
        '''Delete a product'''
        product = self.get_object(uid)
        shop = Shop.objects.get(uid=org_uid)
        if shop.merchant.uid == request.user.uid:
            product.delete()
            return Response({"msg":"Product Successfully Removed"},status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You are not merchant of this organization'}, status=status.HTTP_403_FORBIDDEN)


class ProductSearchView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request ,uid):
        '''Get searched product'''
        shop = Shop.objects.get(uid=uid)
        shop_products = Product.objects.filter(organization=shop)
        search_query = request.query_params.get('product', '')
        products = shop_products.filter(product_name__icontains=search_query)

        if shop.merchant.uid == request.user.uid:
            if products:
                serializer = ProductSerializers(products, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No product found .'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'message': 'You are not merchant of this shop'}, status=status.HTTP_403_FORBIDDEN)
    

class ConnectedShopProduct(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request ,uid):
        '''Get product list of connected organization '''
        # merchant who want to see another merchant shop product
        requested_merchant = request.user

        # find the shop with shop uid and then find the shop product
        shop = Shop.objects.get(uid=uid)
        shop_products = Product.objects.filter(organization=shop)

        # now check if the merchant isn't want to see his own shop product
        if shop.merchant == requested_merchant :
            return Response({'message':'you can not see your own product with this url'},status=status.HTTP_403_FORBIDDEN)

        # now find the connection is exits with requested_merchant shop and target shop
        try: 
            connection = Connection.objects.get(target_shop = shop)
        except Connection.DoesNotExist:
            return Response({'message': 'No Connection Found'}, status=status.HTTP_404_NOT_FOUND)
        
        # now check if the source shop merchant is same as requested merchant and their status is approve or not
        if connection.source_shop.merchant == requested_merchant:
            if connection.status == 'approved':
                if shop_products:
                    # is everything ok we give the access to product 
                    serializer = ProductSerializers(shop_products, many=True)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'No product found for this organization.'}, status=status.HTTP_404_NOT_FOUND)
           
            return Response({'message':"your connection request isn't approved yet"},status=status.HTTP_403_FORBIDDEN)
        
        return Response({'message':"you don't have any connection with this organization"},status=status.HTTP_403_FORBIDDEN)


