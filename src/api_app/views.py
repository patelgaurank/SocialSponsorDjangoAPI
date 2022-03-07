from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
# from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import viewsets, permissions, status
from rest_framework import response
from rest_framework import views
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework import mixins
from rest_framework import generics

from .serializers import UserSerializer, GroupSerializer, UserDataSerializer, AllUsersSerializer, AllUrlSerializer
from .models import UserData, url
from users.models import NewUser

from datetime import datetime

""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""


# @permission_classes((permissions.AllowAny,))
# @api_view(['GET', 'POST'])
class BackendAppOverView(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = url.objects.all()
    # serializer_class = AllUrlSerializer

    # def get_object(self):
    #     return get_object_or_404(url, **filter)

    def get_serializer_class(self):
        print(self.request.user.is_admin)
        if self.request.user.is_admin:
            return AllUrlSerializer

    # def list(self, request, format=None, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     # if request.user:
    #     #     data = {'isLoggedIn': 'No', 'currentUser': '',
    #     #             'result': serializer.data}
    #     # else:
    #     #     data = {'isLoggedIn': 'Yes', 'currentUser': '',
    #     #             'result': serializer.data}
    #     return Response(serializer.data)

    # def retrieve(self, request, format=None, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def list(self, request):
    #     pass

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

    # @action(detail=False, methods=['get'])
    # def retrieve(self, request, *args, **kwargs):
    #     data = {
    #         'List': '/user-list/',
    #         'Detail': '/user-detail/<str:pk>/',
    #         'Create': '/user-create/',
    #         'Update': '/user-update/<str:pk>/',
    #         'Delete': '/user-delete/<str:pk>/',
    #     }
    #     return Response(data)

    # @action(detail=False, methods=['get'])
    # def list(self, request, *args, **kwargs):
    #     data = {
    #         'List': '/user-list/',
    #         'Detail': '/user-detail/<str:pk>/',
    #         'Create': '/user-create/',
    #         'Update': '/user-update/<str:pk>/',
    #         'Delete': '/user-delete/<str:pk>/',
    #     }        

    #     return Response(data)


class PostUserWritePermission(permissions.BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class UserData(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = UserData.objects.all()

    def get_object(self):
        return get_object_or_404(UserData, **filter)

    def get_serializer_class(self):
        return UserDataSerializer

    def list(self, request, format=None, *args, **kwargs):
        print(request)
        pageVisitor(request)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print(request.user)
        if request.user:
            data = {'isLoggedIn': 'No', 'currentUser': '',
                    'result': serializer.data}
        else:
            data = {'isLoggedIn': 'Yes', 'currentUser': '',
                    'result': serializer.data}
        return response(data)

    def retrieve(self, request, format=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response(serializer.data)


class CurrentUserViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = NewUser.objects.all()
    serializer_class = AllUsersSerializer


def pageVisitor(*args, **kwargs):
    request = args[0]
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # print('META KEY - %s' % request.META)
    print('Ip - %s' % ip)
    print('QueryDict - %s' % request.GET)
    print('User - %s' % request.user)
    print('Authenticated - %s' % request.auth)
    print('Authenticator - %s' % request.authenticators)
    print('data - %s' % request.data)
    print('Method - %s' % request.method)
    print('content_type - %s' % request.content_type)
    print('Host - %s' % request.META['HTTP_REFERER']
          if 'HTTP_REFERER' in request.META else 'None')
    print('Page - %s' % request.META['PATH_INFO']
          if 'PATH_INFO' in request.META else 'None')
    print('Agent - %s' % request.META['HTTP_USER_AGENT']
          if 'HTTP_USER_AGENT' in request.META else 'None')
    print('session - %s' % request.session)
    print('body - %s' % request.stream)
    print(request.GET.items())
    for k, v in request.GET.items():
        print(k, v)

# class UserData(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     userdata = UserData.objects.all()

#     def list(self, request):
#         serializer = UserDataSerializer(self.userdata, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = UserDataSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         qs = get_object_or_404(self.userdata, pk=pk)
#         serializer = UserDataSerializer(qs)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         qs = get_object_or_404(self.userdata, pk=pk)
#         serializer = UserDataSerializer(qs, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     userdata = UserData.objects.get(pk=pk)
    #     userdata.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductsListView(generics.ListCreateAPIView):


# @permission_classes((permissions.AllowAny,))
# class UserDataListView(APIView):

#     """
#     Retrieve, update or delete a product instance.
#     """

#     def get(self, request, format=None):
#         print('get -----------------------')
#         qs = UserData.objects.all()
#         serializer = UserDataSerializer(qs, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         print('update -----------------------')
#         serializer = UserDataSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes((permissions.AllowAny,))
# class UserDataDetailsView(APIView):

#     """
#     Retrieve, update or delete a snippet instance.
#     """

#     def get_object(self, pk):
#         try:
#             return UserData.objects.get(Product_Id=pk)
#         except UserData.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         print('Get -----------------------')
#         qs = self.get_object(pk)
#         serializer = UserDataSerializer(qs)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         print('put ----------------------- %s' % (pk))
#         qs = self.get_object(pk)
#         serializer = UserDataSerializer(qs, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         print('delete -----------------------')
#         qs = self.get_object(pk)
#         qs.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @permission_classes([IsAuthenticated])
# @api_view(['GET', 'POST'])
# def userdata_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         userdata = UserData.objects.all()
#         serializer = UserDataSerializer(userdata, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UserDataSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # @permission_classes((permissions.AllowAny,))
# @permission_classes([IsAuthenticated])
# @ api_view(['GET', 'PUT', 'DELETE'])
# def userdata_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """

#     try:
#         userdata = UserData.objects.get(pk=pk)
#     except UserData.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserDataSerializer(userdata)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserDataSerializer(userdata, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         userdata.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
