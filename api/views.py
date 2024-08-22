from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .models import SpamNumber

import logging

logger = logging.getLogger(__name__)

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    logger.debug(f"Login attempt with username: {username}")

    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            logger.debug(f"Authenticated user: {user}, User ID: {user.id}")
            token, created = Token.objects.get_or_create(user=user)
            logger.debug(f"Token created: {token.key}, Created: {created}")
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Token creation error: {str(e)}")
            return Response({'error': f'Database error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    logger.warning(f"Invalid login attempt for username: {username}")
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mark_as_spam(request):
    phone_number = request.data.get('phone_number')
    if phone_number:
        spam_number, created = SpamNumber.objects.get_or_create(phone_number=phone_number)
        if created:
            spam_number.marked_as_spam = True
            spam_number.save()
            return Response({'message': 'Number marked as spam'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Number is already marked as spam'}, status=status.HTTP_200_OK)
    return Response({'error': 'Phone number not provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unmark_as_spam(request):
    phone_number = request.data.get('phone_number')
    if phone_number:
        try:
            spam_number = SpamNumber.objects.get(phone_number=phone_number)
            spam_number.marked_as_spam = False
            spam_number.save()
            return Response({'message': 'Number unmarked as spam'}, status=status.HTTP_200_OK)
        except SpamNumber.DoesNotExist:
            return Response({'error': 'Number not found in spam list'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Phone number not provided'}, status=status.HTTP_400_BAD_REQUEST)