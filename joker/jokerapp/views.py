from datetime import datetime
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from jokerapp.models import Booking, Room, User
from jokerapp.serializer import BookingSerializer, RoomSerializer, UserSerializer, UserRegisterSerializer, \
    UserLoginSerializer


from jokerapp.validations import validate_username, validate_password, custom_validation


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    ##
    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            user_data = {
                'id': user.id,
                'username': user.username,
                'userRole': user.userrole}
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    ##
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def BookApi(request):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Booking added successfully", safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def RoomApi(request):
    if request.method == 'GET':
        categories = Room.objects.all()
        categories_serializer = RoomSerializer(categories, many=True)
        return JsonResponse(categories_serializer.data, safe=False)

    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = RoomSerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("room added successfully", safe=False)
        return JsonResponse('Failed to add Category', safe=False)


@csrf_exempt
def AvailableRoomsApi(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return JsonResponse({'error': 'Both start_date and end_date parameters are required.'}, status=400)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')

        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Please use YYYY-MM-DD HH:MM:SS.'}, status=400)

        all_rooms = Room.objects.all()
        available_rooms = []
        for room in all_rooms:
            existing_bookings = Booking.objects.filter(
                room=room,
                start_time__lte=end_date,
                end_time__gte=start_date
            )
            if not existing_bookings.exists():
                available_rooms.append(room)

        serializer = RoomSerializer(available_rooms, many=True)
        return JsonResponse(serializer.data, safe=False)


class RoomListApi(APIView):

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):
    def delete(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            room.delete()
            return Response('Room deleted successfully', status=status.HTTP_204_NO_CONTENT)
        except Room.DoesNotExist:
            return Response('Room not found', status=status.HTTP_404_NOT_FOUND)



