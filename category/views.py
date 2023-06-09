from category.serializers import CategorySerializers
from category.models import Category
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account_api.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

# Api view for category start

class CategoryList(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializers(category, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @extend_schema(
    request=CategorySerializers,
    responses={201: CategorySerializers},
    )
    def post(self, request, format=None):
        # Check if user is admin or not
        if not request.user.is_admin:
            return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Category Added Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get_object(self, uid):
        try:
            return Category.objects.get(uid=uid)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, uid, format=None):
        category = self.get_object(uid)
        serializer = CategorySerializers(category)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @extend_schema(
    request=CategorySerializers,
    responses={201: CategorySerializers},
    )
    def put(self, request,uid, format=None):
        # Check if user is admin or not
        if not request.user.is_admin:
            return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object(uid)
        serializer = CategorySerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Category Update Sucessfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,uid, format=None):
        # Check if user is admin or not
        if not request.user.is_admin:
            return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object(uid)
        category.delete()
        return Response({"message":"Category Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)
    
# Api view for category end