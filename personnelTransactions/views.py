from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Personnel


class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            unit_id = request.data.get('unit', None)
            personnel_data = {'unit': unit_id, 'user': user.id}

            personnel_serializer = PersonnelSerializer(data=personnel_data)
            if personnel_serializer.is_valid():
                personnel_serializer.save()

                return Response(user_serializer.data, status=status.HTTP_201_CREATED)

            # PersonnelSerializer geçerli değilse, hata ayrıntılarını görüntüleyin
            return Response({"error": "PersonnelSerializer is not valid", "details": personnel_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        # CustomUserSerializer geçerli değilse, hata ayrıntılarını görüntüleyin
        return Response({"error": "CustomUserSerializer is not valid", "details": user_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class UserIdList(APIView):
        def get(self, request, unit_id=None):
            # Assuming you receive the unit_id as a parameter in the URL
            if unit_id is not None:
                movements = CustomUser.objects.filter(unit__id=unit_id, is_active=True)
            else:
                movements = CustomUser.objects.filter(is_active=True)

            serializer = UserSerializer(movements, many=True)
            return Response(serializer.data)


class UserList(APIView):
    def get(self, request):
        movements = CustomUser.objects.filter(is_active=True)
        serializer = UserSerializer(movements, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitList(APIView):
    def get(self, request):
        movements = Unit.objects.all()
        serializer = PersonnelUnitSerializer(movements, many=True)
        return Response(serializer.data)


class UnitListCreateAPIView(APIView):
    def get(self, request):
        units = Unit.objects.all()
        serializer = PersonnelUnitSerializer(units, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonnelUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Unit, pk=pk)

    def get(self, request, pk):
        unit = self.get_object(pk)
        serializer = PersonnelUnitSerializer(unit)
        return Response(serializer.data)

    def put(self, request, pk):
        unit = self.get_object(pk)
        serializer = PersonnelUnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        unit = self.get_object(pk)
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['personnelTransactions']
        data = CustomUser.objects.filter(id=user.id)
        # Kullanıcı bilgilerini istediğiniz şekilde alabilir ve serialize edebilirsiniz
        user_data = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'unit_id': user.unit_id,
        }

        # Token oluştur
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data,   # Kullanıcı bilgilerini ekleyin
        }, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logout successful"})



class SubUnitsByUpperUnitAPIView(APIView):
    def get(self, request, upper_unit_id):
        try:
            upper_unit = Unit.objects.get(id=upper_unit_id)
            sub_units = upper_unit.sub_units.all()
            serializer = UnitSerializer(sub_units, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response({"error": "Upper unit not found"}, status=status.HTTP_404_NOT_FOUND)