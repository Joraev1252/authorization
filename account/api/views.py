from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from . import serializers
from account.models import Account
from account.api.serializers import AccountSerializers, RegistrationSerializer, ActivateAccountSerializer, DeactivateAccountSerializer

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView

@api_view(['POST', ])
def account_register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered a new user."
            data['email'] = account.email
            # data['username'] = account.username
            refresh = RefreshToken.for_user(account)
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors
        return Response(data)


@api_view(["POST"])
def account_login(request):
    if request.method == "POST":
        email = request.data["email"]
        password = request.data["password"]
        authenticated_user = authenticate(request, email=email, password=password)
        if authenticated_user != None:
            # if (authenticated_user.is_authenticated and authenticated_user.is_superuser):
            if authenticated_user.is_authenticated:
                login(request, authenticated_user)
                return JsonResponse({"Message": "User is Authenticated. "})
            else:
                return JsonResponse({"message": "User is not authenticated. "})
        else:
            return JsonResponse({"Message": "Either User is not registered or password does not match"})


@api_view(["POST"])
def account_logout(request):
    print(request.user)
    logout(request)
    return JsonResponse({"message": "LoggedOut"})


@api_view(['GET', ])
def accounts_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            accounts = Account.objects.all()
            serializer = AccountSerializers(accounts, many=True)
            return Response(serializer.data)
    else:
        return Response({'message': 'Please authenticate!'})


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = AccountSerializers(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account update success"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def user_delete(request, pk):
    user = Account.objects.get(id=pk)
    user.delete()
    return Response('User successfully deleted!')



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def deactivate_account_view(request, pk):

    if request.method == 'POST':
        accounts = Account.objects.get(id=pk)
        serializer = DeactivateAccountSerializer(accounts, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account has been deactivated!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def activate_account_view(request, pk):

    if request.method == 'POST':
        accounts = Account.objects.get(id=pk)
        serializer = ActivateAccountSerializer(accounts, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account has been activated!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



