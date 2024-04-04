from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class CustomUserManager(UserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('You havent provided a username')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLE_CHOICES = (
        ('normal', 'Normal'),
        ('superuser', 'Superuser'),
    )
    userrole = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='normal')

    username = models.CharField(max_length=40, unique=True)  # Ensure unique username

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # No email required

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()




    def is_booked(self, start_time, end_time):

        conflicting_bookings = Booking.objects.filter(
            room=self,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        return conflicting_bookings.exists()







class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"Booking for {self.room.name} from {self.start_time} to {self.end_time}"
