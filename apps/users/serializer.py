from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField


class RegisterSerializer(serializers.Serializer):
    last_name = serializers.CharField(min_length=6)
    first_name = serializers.CharField(min_length=6)
    birth_date = serializers.DateField()
    phone_number = PhoneNumberField(region="KG")
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
