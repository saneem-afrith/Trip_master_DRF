from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from tripmaster.models import Tripdb
from tripmaster.serializers import TripSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import authentication, permissions, serializers

# Create your views here.
class SignupView(APIView):
    def post(self, request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message": "user created successfully."}, status=201)
        else:
            return Response(data=serializer_instance.errors, status=400)

class TripListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):
        qs = Tripdb.objects.all()
        serializer_instance = TripSerializer(qs, many=True)
        return Response(data=serializer_instance.data, status=200)

    def post(self, request):
        form_data = request.data
        serializer_instance = TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={"message": "Trip created successfully.", "trip": serializer_instance.data}, status=201)
        else:
            return Response(data=serializer_instance.errors, status=400)

class CreateUpdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        trip_object = get_object_or_404(Tripdb, id=id)
        if trip_object.created_by == request.user:
            serializer_instance = TripSerializer(trip_object)
            return Response(serializer_instance.data, status=200)
        else:
            return Response({"message": "You are not the owner of this trip."}) 

    def put(self, request, id ):
        trip_object = get_object_or_404(Tripdb, id=id)
        if trip_object.created_by == request.user:
            raise serializers.ValidationError("You are not the owner of this trip.")

        form_data = request.data
        serializer_instance = TripSerializer(instance=trip_object, data=form_data,)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"message": "Trip updated successfully.", "updated trip": serializer_instance.data}, status=200) 
        else:
            return Response(data=serializer_instance.errors, status=400)

    def delete(self, request, id):
        trip_object = get_object_or_404(Tripdb, id=id)
        if trip_object.created_by != request.user:
            raise serializers.ValidationError("You are not the owner of this trip.")
        trip_object.delete()
        return Response(data={"message": "Trip deleted successfully."}, status=200)
        