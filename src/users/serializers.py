# from typing_extensions import Required
from rest_framework import serializers
from users.models import NewUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from codes.models import Code


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)


    #     # Add custom claims
    #     token['name'] = user.email
    #     # Add more custom fields from your custom user model, If you have a
    #     # custom user model.
    #     # ...
    #     data = {'name': 'gp', 'token': token}
    #     print(data)
    #     return data

    def validate(self, attrs):        
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        # Custom data you want to include
        data.update({'name': self.user.user_name})
        data.update({'email': self.user.email})

        # finduser = Code.objects.filter(user=self.user)
        # if finduser:
        #     Code.objects.filter(user=self.user).delete()           
        # Code.objects.create(user=self.user)
        # and everything else you want to send in the response
        return data

class FindUserActiveOrNotSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('email', 'is_active', 'is_staff')


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
