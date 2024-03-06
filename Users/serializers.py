from .models import Otp
from rest_framework import serializers
from Users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.user_name = validated_data.get(
            'user_name', instance.user_name)

        # Update password if provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        # Save the updated instance
        instance.save()
        return instance


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['id', 'created_for', 'code', 'created_at']
