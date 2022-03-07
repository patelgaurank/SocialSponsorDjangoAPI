# from django.http.response import JsonResponse
# from django.core import mail
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
# from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import JsonResponse
import requests
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import DomElementSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
# from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, Token
# from users.models import NewUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import DomElement
# from users.models import AuditEntry
# from codes.models import Code
# from django.contrib.auth import authenticate, login, logout
# import requests, json, os
# from django.utils import timezone
# from datetime import datetime
# import users.email as cEmail
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
import json
# Create your views here.


class CategoryData(viewsets.ViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = DomElementSerializer
    # queryset = DomElement.objects.all()

    def get_serializer_class(self):
        # if self.action == 'update':
        #     return CategoryPUTSerializer
        return DomElementSerializer

    def get_queryset(self):
        if len(self.request.query_params) > 0:
            filter = self.request.query_params
            filterdict = {}
            for k in list(filter.keys()):
                filterdict[k]=filter[k]

            queryset = DomElement.objects.filter(**filterdict)
            if len(queryset) > 0:                    
                return queryset
            return Response({'detail':"Wrong request"}, status=status.HTTP_400_BAD_REQUEST)
        return {'detail':"No data found"}

    def list(self, request, *args, **kwargs):

        if len(request.query_params) > 0:
            filter = request.query_params
            filterdict = {}
            for k in list(filter.keys()):
                filterdict[k]=filter[k]
            queryset = DomElement.objects.filter(**filterdict)
            if len(queryset) > 0:                    
                serializer = DomElementSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail':"Wrong request"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':"No data found"}, status=status.HTTP_400_BAD_REQUEST)

    # def get_object(self):
    #     obj = get_object_or_404(self.get_queryset(),
    #                             pk=self.kwargs["pk"], **filter)
    #     return super().get_object()
    # def get_object(self):        
    #     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    # def get_object(self):
    #     # filter = {}
    #     # if self.kwargs['pk'].find("&"):
    #     #     for field in self.kwargs['pk'].split("&"):
    #     #         filter[field.split(':')[0]] = field.replace(
    #     #             '"', '').split(':')[1]
    #     filterFild = (self.kwargs['pk']).split('=')[0]
    #     filterValue = (self.kwargs['pk']).split('=')[1].replace('"', "")
    #     filter = {filterFild: filterValue}
    #     obj = get_object_or_404(self.get_queryset(),
    #                             pk=self.kwargs["pk"], **filter)
    #     return obj

    # def list(self, request, *args, **kwargs):
    #     for k, v in request.GET.items():
    #         print(k, v)
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     print(self.check_object_permissions(self.request, page))
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def retrieve(self, request, format=None, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # def destroy(self, request, pk=None):
    #     pass
