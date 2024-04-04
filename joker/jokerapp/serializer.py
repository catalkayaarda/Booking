from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from jokerapp.models import Room, Booking, User

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(username=clean_data['username'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    ##
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'userrole')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'start_time', 'end_time']

    def validate(self, data):
        room = data.get('room')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        overlapping_bookings = Booking.objects.filter(room=room, start_time__lt=end_time, end_time__gt=start_time)
        if overlapping_bookings.exists():
            raise serializers.ValidationError("Booking overlaps with existing booking")

        return data


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity']
