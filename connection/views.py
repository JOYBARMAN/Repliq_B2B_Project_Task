from connection.serializers import ConnectionSerializers,SendConnectionSerializers,ConnectionActionSerializers
from shop.serializers import ShopSerializers
from shop.models import Shop
from category.models import Category
from account_api.models import User
from connection.models import Connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_api.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.db.models import Q
from drf_spectacular.utils import extend_schema




class SendConnectionView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    # @extend_schema(
    # request=SendConnectionSerializers,
    # responses={201: SendConnectionSerializers},
    # )

    def post(self, request,target_shop_uid):

        # first get the sender and receiver information
        sender = request.user
        receiver = Shop.objects.get(uid=target_shop_uid)

        try:
            # find sender active shop
            sender_active_shop = Shop.objects.get(merchant=sender, is_active=True)
        except Shop.DoesNotExist:
            # No active shop found for the sender
            return Response({'message': 'You do not have any active shop.'}, status=status.HTTP_404_NOT_FOUND)
        
        # now find if the both shop merchant isn't same ?
        if sender_active_shop.merchant != receiver.merchant:
             # Check if the sender's active shop has the same category as the receiver's shop
            if sender_active_shop.category == receiver.category:
                data={
                    "source_shop":sender_active_shop.id,
                    "target_shop":receiver.id,
                }
                serializer = SendConnectionSerializers(data=data)
                serializer.is_valid()
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Connection sent successfully.'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # The sender and receiver have different categories
                return Response({'message': 'The sender and receiver is not same category'}, status=status.HTTP_400_BAD_REQUEST)
        
            # The sender and receiver have the same merchant
        return Response({'message': 'You cannot send a connection to your own shop.'}, status=status.HTTP_400_BAD_REQUEST)


class ConnectionRequest(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        merchant = request.user
        connection_request = Connection.objects.filter(target_shop__merchant=merchant)
        if connection_request:
            serializer = ConnectionSerializers(connection_request, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'message': "You don't have any connection request yet" }, status=status.HTTP_404_NOT_FOUND) 


class ConnectionRequestAction(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=ConnectionActionSerializers,
    responses={201: ConnectionActionSerializers},
    )

    def post(self,request,connection_uid):
        try:
            connection= Connection.objects.get(uid=connection_uid)
        except Connection.DoesNotExist:
            return Response({'message': 'Connection not found '}, status=status.HTTP_400_BAD_REQUEST)
       
        #now check if the merchant is target shop merchant
        if connection.target_shop.merchant != request.user:
            return Response({'message': "You are not proper merchant to do this action" }, status=status.HTTP_404_NOT_FOUND) 


        serializer = ConnectionActionSerializers(data=request.data)
        
        if serializer.is_valid():
            connection.status = serializer.validated_data['status']
            connection.save()
            return Response({"msg": "Status Cahnged Sucessfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ConnectedShopView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request, shop_uid):
        # now find which shop are connected with this shop_uid
        try:
            connected_shops = Connection.objects.filter(Q(source_shop__uid=shop_uid) | Q(target_shop__uid=shop_uid),status="approved")
        
        except Connection.DoesNotExist:
            return Response({'message': 'You dont have any connection yet'}, status=status.HTTP_400_BAD_REQUEST)
        
        if connected_shops:
            serializer = ConnectionSerializers(connected_shops, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response({'message': "No connected shop found" }, status=status.HTTP_404_NOT_FOUND) 

        # if connected_shops:
        #     shop_data_list = []
        #     # here i have connection model data . now i have to find shop which uid is not equal to pssing shop_uid , so that i can pass only connected shop data in shop serializers 

        #     for shop in connected_shops:
        #         if shop.source_shop.uid != shop_uid:
        #             shop_data = Shop.objects.get(uid=shop.source_shop.uid)
        #             shop_data_list.append(shop_data)

        #         else:
        #             shop_data = Shop.objects.get(uid=shop.target_shop.uid)
        #             shop_data_list.append(shop_data)
            
        #     serializer = ShopSerializers(shop_data_list,many=True)
        #     return Response(serializer.data,status=status.HTTP_200_OK)
        
        # return Response({'message': "You don't have any connected shop" }, status=status.HTTP_404_NOT_FOUND) 