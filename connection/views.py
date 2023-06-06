from connection.serializers import ConnectionSerializers,SendConnectionSerializers,ConnectionActionSerializers
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



class SendConnectionView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

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