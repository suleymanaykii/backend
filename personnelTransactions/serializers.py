
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'name', 'surname', 'district', 'unit', 'neighbourhood')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}  # 'required' burada False olarak ayarlandı

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)

        # Parola verisi gönderilmişse veya None değilse, parolayı ayarla
        password = '12345'
        user.password = make_password(password)
        user.save()

        return user


class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class PersonnelUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class PersonnelMovementsSerializer(serializers.ModelSerializer):
    unit = AuthorSerializer()
    class Meta:
        model = Personnel
        fields = ['uuid', 'name', 'surname', 'email', 'address', 'phone', 'unit', 'user', 'created_at', 'updated_at', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError('User not found')
        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')
        data['personnelTransactions'] = user
        return data

class RecursiveUnitSerializer(serializers.ModelSerializer):
    sub_units = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'name', 'sub_units']

    def get_sub_units(self, obj):
        sub_units = Unit.objects.filter(upper_unit=obj)
        serializer = RecursiveUnitSerializer(sub_units, many=True)
        return serializer.data


class UnitSerializer(serializers.ModelSerializer):
    sub_units = RecursiveUnitSerializer(many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ['id', 'name', 'sub_units']