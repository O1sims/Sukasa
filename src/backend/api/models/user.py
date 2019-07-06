from rest_framework import serializers


class LoginModel(serializers.Serializer):
    username = serializers.CharField(
        required=True)
    password = serializers.CharField(
        required=True)


class UserModel(serializers.Serializer):
    username = serializers.CharField(
        min_length=5,
        required=True)
    password = serializers.CharField(
        min_length=8,
        required=True)
    first_name = serializers.CharField(
        required=True)
    second_name = serializers.CharField(
        required=True)
    email = serializers.EmailField(
        required=True)
    avatar = serializers.ImageField(
        required=False)
