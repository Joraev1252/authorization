from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Account


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
                  'email',
                  'full_name',
                  'user_name',
                  'phone_number'
                  ]


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email',
                  'full_name',
                  'user_name',
                  'phone_number',
                  'password',
                  'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            full_name=self.validated_data['full_name'],
            user_name=self.validated_data['user_name'],
            phone_number=self.validated_data['phone_number']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match!'})
        account.set_password(password)
        account.save()
        return account


# class TokenObtainPairSerializer(TokenObtainSerializer):
#     @classmethod
#     def get_token(cls, user):
#         return RefreshToken.for_user(user)
#
#     def validate(self, attrs):
#         data = super().validate(attrs)
#
#         refresh = self.get_token(self.user)
#
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#
#         return data



class DeactivateAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['is_active']

    def update(self, instance, validated_data):
        instance.is_admin = False
        instance.is_active = False
        instance.is_staff = False
        instance.is_superuser = False
        instance.is_superuser = False
        instance.save()
        return instance



class ActivateAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['is_active']

    def update(self, instance, validated_data):
        instance.is_admin = False
        instance.is_active = True
        instance.is_staff = False
        instance.is_superuser = False
        instance.is_superuser = False
        instance.save()
        return instance