from math import perm
from django.http.response import JsonResponse
from django.core import mail
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from .serializers import CustomUserSerializer, FindUserActiveOrNotSerializer, MyTokenObtainPairSerializer, PhoneNumberSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, Token
from users.models import NewUser, NewUserAddress
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import AuditEntry
from codes.models import Code
from django.contrib.auth import authenticate, login, logout
import requests, json, os
from django.utils import timezone
from datetime import datetime
import users.email as cEmail

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:                
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FindUserExistOrNot(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        if request.data:
            email = request.data["email"];
            phonenumber = request.data["phonenumber"]
        elif request.query_params:
            email = request.query_params['email'];
            phonenumber = request.query_params['phonenumber']
        if email:
            user = NewUser.objects.filter(email=email)
            print(f'Total phone number connected to this id : {len(user.values("phone_number"))}')
            # if len(user.values("phone_number")) > 1:
            #     return Response(data={})
            print(list(user.values("phone_number"))[0])
            pn = PhoneNumberSerializer(list(user.values("phone_number"))[0])
            print(pn.data)
            userphonenumber = NewUser.objects.filter(email=email, phone_number=phonenumber)            
            if user:
                if userphonenumber:
                    NUser = NewUser.objects.get(email=email, phone_number=phonenumber)
                    finduser = Code.objects.filter(user=NUser)
                    if finduser:
                        Code.objects.filter(user=NUser).delete()
                    Code.objects.create(user=NUser)
                    findusercode = Code.objects.filter(user=NUser).only('number')
                    msg = mail.EmailMessage('Access Code', cEmail.emailbody(email, str(findusercode[0]), email), 'satsangauto@gmail.com', [email])
                    msg.content_subtype = "html"
                    msg.send()                   
                    return Response(data={'detail':'user found','phone_number_to_validate':'***-***-9675'}, status=status.HTTP_302_FOUND)
                return Response(data={'detail':"Phone number is not valid"}, status=status.HTTP_302_FOUND)
            
            data = {"email":email,"phone_number":phonenumber, "password":"DoNotOpen75"}
            serializer = CustomUserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    NUser = NewUser.objects.get(email=email, phone_number=phonenumber)
                    json = serializer.data
                    finduser = Code.objects.filter(user=NUser)
                    if finduser:
                        Code.objects.filter(user=NUser).delete()           
                    Code.objects.create(user=NUser)
                    findusercode = Code.objects.filter(user=NUser).only('number')
                    msg = mail.EmailMessage('Access Code', cEmail.emailbody(email, str(findusercode[0]), email), 'satsangauto@gmail.com', [email])
                    msg.content_subtype = "html"
                    msg.send()
                    return Response(data={'detail':'New user created'}, status=status.HTTP_201_CREATED)                
            return Response(data={'detail':'User not valid. Try again!'}, status=status.HTTP_302_FOUND)
        return Response(data={'detail':'Email is missing. Try again!'}, status=status.HTTP_302_FOUND)

class ValidateCode(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        if request.data:
            email = request.data["email"]; phonenumber = request.data["phonenumber"]; code = request.data["code"]
        elif request.query_params:
            email = request.query_params['email']; phonenumber = request.query_params['phonenumber']; code = request.query_params["code"]
        if email:
            user = NewUser.objects.filter(email=email)
            userphonenumber = NewUser.objects.filter(email=email, phone_number=phonenumber)            
            if user:
                if userphonenumber:
                    NUser = NewUser.objects.get(email=email, phone_number=phonenumber)
                    if len(Code.objects.filter(user=NUser)) > 0:
                        codetolookfor = Code.objects.get(user=NUser)
                        codedatestamp = Code.objects.get(user=NUser).created_at
                        datetimenow=datetime.utcnow().replace(tzinfo=timezone.utc)
                        if (datetimenow - codedatestamp).total_seconds() < 300:
                            if str(codetolookfor) == str(code):
                                url = request.scheme + '://' + request.META['HTTP_HOST'] + '/api/token/'
                                payload = json.dumps({
                                "email": email,
                                "password": "DoNotOpen75"
                                })
                                headers = {
                                'Content-Type': 'application/json',
                                'Cookie': 'csrftoken=ohV8HrC4xIzYk7aijQGXmMmh3pFlBlUDA3Nn8Irf1jeqq7GpkYWo6hLMqLTPYuvT'
                                }
                                r = requests.request("POST", url, headers=headers, data=payload).json()
                                r["detail"]="Succeed!"
                                return Response(data=r, status=status.HTTP_200_OK)
                            codetolookfor.codeentertimer = codetolookfor.codeentertimer+1
                            codetolookfor.save()
                            if Code.objects.get(user=NUser).codeentertimer > 3:
                                Code.objects.filter(user=NUser).delete()
                                return Response(data={'detail':"Please re-request code. Wrong code entered multiple times."}, status=status.HTTP_401_UNAUTHORIZED)
                            return Response(data={'detail':"Code doesn't matched. Please renter."}, status=status.HTTP_401_UNAUTHORIZED)
                        return Response(data={'detail':"Please re-request code."}, status=status.HTTP_401_UNAUTHORIZED)
                    return Response(data={'detail':"Please re-request code."}, status=status.HTTP_401_UNAUTHORIZED)
                return Response(data={'detail':"Phone number is not valid. Try again!"}, status=status.HTTP_302_FOUND)
            return Response(data={'detail':'User not valid. Try again!'}, status=status.HTTP_302_FOUND)
        return Response(data={'detail':'Email is not valid. Try again!'}, status=status.HTTP_302_FOUND)

class FindUserLogOut(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # simply delete the token to force a login
        if request.data:
            email = request.data["email"]; phonenumber = request.data["phonenumber"]
        elif request.query_params:
            email = request.query_params['email']; phonenumber = request.query_params['phonenumber']
        if email:
            user = NewUser.objects.filter(email=email)
            userphonenumber = NewUser.objects.filter(email=email, phone_number=phonenumber)
            if user:
                if userphonenumber:
                    loginuser = authenticate(email=email,password="DoNotOpen75")
                    login(request,loginuser)
                    logout(request)
                    # request.user.auth_token.delete()
                    return Response(status=status.HTTP_200_OK)
        return Response(data={'detail':'Something went wrong. Try again!'}, status=status.HTTP_406_NOT_ACCEPTABLE)    
        # return Response(data={'detail':'Something went wrong. Try again!'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class FindUserAddress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        email = request.user.email
        phonenumber = request.user.phone_number
        isadmin = request.user.is_admin
        isstaff = request.user.is_staff
        isactive = request.user.is_active
        alertcount = 0; alertmessage = None
        if email:
            user = NewUser.objects.filter(email=email)            
            if user:
                userphonenumber = user.filter(phone_number=phonenumber)
                if userphonenumber:
                    useraddressbyemail = NewUserAddress.objects.filter(email=email)
                    if len(userphonenumber.values('user_name')) == 0 or userphonenumber.values('user_name')[0]['user_name'] == '':
                        alertcount += 1
                        alertmessage = 'Please update User name.'
                    if len(useraddressbyemail) == 0:
                        alertcount += 1
                        alertmessage = f"{alertmessage}\nPlease update address."                    
                    return Response(data={'detail':f'{email} authenticated.', 'alertmessage':alertmessage, 'alertcount':alertcount}, status=status.HTTP_200_OK)
                return Response(data={'detail':'User found and authenticated.'}, status=status.HTTP_200_OK)
        return Response(data={'detail':'Something went wrong. Try again!'}, status=status.HTTP_406_NOT_ACCEPTABLE)    
    # return Response(data={'detail':'user is not authencated'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class ValidateUserAndPhoneNumber(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        if request.data["email"]:
            user = NewUser.objects.filter(email=request.data["email"]).values()
            print(user[0]['phone_number'])
            if user:
                return Response([{'detail':'user found'}], status=status.HTTP_302_FOUND)
            
            # return Response(json, status=status.HTTP_201_CREATED)                
            return Response([{'detail':'user not found'}], status=status.HTTP_404_NOT_FOUND)
        return Response([{'detail':'Email is missing.'}], status=status.HTTP_204_NO_CONTENT)

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]    
    serializer_class = MyTokenObtainPairSerializer
    # def get_serializer_class(self):
    #     return MyTokenObtainPairSerializer

    # def post(self, request, *args, **kwargs):
    #     user = request.data.get('email', {})
    #     print(user)
    #     serializer = self.serializer_class()
    #     data = {'name': 'gp', 'token': serializer.data}
    #     print(data)
    #     # serializer = self.get_serializer(instance)
    #     # return Response(serializer.data)
    #     return Response(data)

class FindUserActiveOrNot(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return FindUserActiveOrNotSerializer

    def get_queryset(self):
        queryset = NewUser.objects.all()
        return queryset

    def retrieve(self, request, format='json', *args, **kwargs):
        # print(self.kwargs['pk'])
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer, status=status.HTTP_302_FOUND)

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            if request.data:
                email = request.data["email"]; phonenumber = request.data["phonenumber"]
                refresh = request.data["refresh"]
            elif request.query_params:
                email = request.query_params['email']; phonenumber = request.query_params['phonenumber']
                refresh = request.query_params["refresh"]
            if email:
                user = NewUser.objects.filter(email=email)
                userphonenumber = NewUser.objects.filter(email=email, phone_number=phonenumber)                            
                if user:
                    if userphonenumber:
                        NUser = NewUser.objects.get(email=email, phone_number=phonenumber)
                        finduser = Code.objects.filter(user=NUser)
                        if finduser:
                            Code.objects.filter(user=NUser).delete()
                        token = RefreshToken(refresh)
                        # if not token.check_blacklist:
                        token.blacklist()
                        return Response(data={'detail':"Log out sucessfully!"}, status=status.HTTP_205_RESET_CONTENT)
                    return Response(data={'detail':"Phone number is not valid. Try again!"}, status=status.HTTP_302_FOUND)
                return Response(data={'detail':'User not valid. Try again!'}, status=status.HTTP_302_FOUND)
            return Response(data={'detail':'Email is not valid. Try again!'}, status=status.HTTP_302_FOUND)
        except Exception as e:
            return Response(data={'detail':'Please login back.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format='json'):
        print(request)
        try:
            if request.data:
                email = request.data["email"]; phonenumber = request.data["phonenumber"]
                refresh_token = request.data["refresh_token"]
            elif request.query_params:
                email = request.query_params['email']; phonenumber = request.query_params['phonenumber']
                refresh_token = request.query_params["refresh_token"]
            if email:
                user = NewUser.objects.filter(email=email)
                userphonenumber = NewUser.objects.filter(email=email, phone_number=phonenumber)                            
                if user:                    
                    if userphonenumber:
                        NUser = NewUser.objects.get(email=email, phone_number=phonenumber)
                        finduser = Code.objects.filter(user=NUser)
                        if finduser:
                            Code.objects.filter(user=NUser).delete()
                        # print(OutstandingToken(token=refresh_token))
                        token = RefreshToken(token=refresh_token)
                        token.blacklist()                                                                                    
                        return Response(status=status.HTTP_205_RESET_CONTENT)
                    return Response(data={'detail':"Phone number is not valid. Try again!"}, status=status.HTTP_302_FOUND)
                return Response(data={'detail':'User not valid. Try again!'}, status=status.HTTP_302_FOUND)
            return Response(data={'detail':'Email is not valid. Try again!'}, status=status.HTTP_302_FOUND)
        except Exception as e:
            # data={'detail':e.args[0]}, 
            return Response(data={'detail':'Please login back.'}, status=status.HTTP_400_BAD_REQUEST)