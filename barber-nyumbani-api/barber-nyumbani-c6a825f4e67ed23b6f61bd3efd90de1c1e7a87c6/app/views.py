from django.shortcuts import render

from app.permissions import IsAdminOrReadOnly
from .models import Service, Barber, Appointment
from django.contrib.auth.models import User

# authentication
from django.contrib.auth import authenticate, login, logout


from decouple import config, Csv


# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, UserCreateSerializer, ServiceSerializer, ServiceCreateSerializer, BarberSerializer, BarberCreateSerializer, AppointmentSerializer, AppointmentCreateSerializer, ApproveAppointmentSerializer
from .permissions import IsAdminOrReadOnly


# sending of sms messages
import africastalking

username = config('AFRICASTALKING_USERNAME')
api_key = config('AFRICASTALKING_API_KEY')

africastalking.initialize(username, api_key)

# Initialize the SMS service
sms = africastalking.SMS


def index(request):
    return render(request, 'index.html')


# rest api ====================================

class UserList(APIView):  # list all users
    """
    List all users.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserCreate(APIView):  # create user
    """
    Create a user.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login user ====================================
class loginUser(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# logout user ====================================
class logoutUser(APIView):  # logout user
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


# services ====================================
class ServiceList(APIView):  # list all services
    """
    List all services.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):  # get all services
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # create service
        serializer = ServiceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetail(APIView):  # get service by id
    """
    Retrieve, update or delete a service instance.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# barbers ====================================
class BarberList(APIView):  # list all barbers
    """
    List all barbers.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):  # get all barbers
        barbers = Barber.objects.all()
        serializer = BarberSerializer(barbers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # create barber
        serializer = BarberCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BarberDetail(APIView):  # get barber by id
    """
    Retrieve, update or delete a barber instance.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self, pk):
        try:
            return Barber.objects.get(pk=pk)
        except Barber.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        barber = self.get_object(pk)
        serializer = BarberSerializer(barber)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        barber = self.get_object(pk)
        serializer = BarberSerializer(barber, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        barber = self.get_object(pk)
        barber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# appointments ====================================
class AppointmentList(APIView):  # list all appointments
    """
    List all appointments.
    """
    permission_classes = (IsAdminOrReadOnly,)

    # show either error message for sending sms or success message
    def on_finish(error, response):
        if error is not None:
            raise error
        print(response)

    def get(self, request, format=None):  # get all appointments
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # create appointment
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # get the phone number from the appointment and send sms
            phone_number = serializer.data['phone']
            message = "Hey there, Your appointment has been created. You will receive a confirmation message shortly."
            sms.send(message, [phone_number], callback=self.on_finish)
            # get the admin phone number and send sms ============================
            # admin_phone_number = User.objects.get(username='admin').phone
            # sms.send("New appointment created ", [admin_phone_number], callback=self.on_finish)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(APIView):  # get appointment by id
    """
    Retrieve, update or delete a appointment instance.
    """
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        appointment = self.get_object(pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# approve appointment ====================================
class ApproveAppointmentView(APIView):  # get appointment by id
    """
    update appointment instance.
    """
    permission_classes = (IsAdminOrReadOnly,)

    # show either error message for sending sms or success message
    def on_finish(error, response):
        if error is not None:
            raise error
        print(response)

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = ApproveAppointmentSerializer(
            appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # get the phone number from the appointment and send sms
            phone_number = serializer.data['phone']
            message = "Hey there, Your appointment has been approved."
            sms.send(message, [phone_number], callback=self.on_finish)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
