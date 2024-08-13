from rest_framework import serializers
from . import models


# creating the serializer class for the user model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'mobile_number', 'address', 'nic', 'branch', 'first_name',
                  'last_name', 'password']

    # for password validations
    def create(self, validated_data):
        # Extract the password from the validated data
        password = validated_data.pop('password', None)

        # Create the user instance without setting the password yet
        user = models.CustomUser(**validated_data)

        # Set the password using Django's set_password method
        if password:
            user.set_password(password)

        # Save the user instance
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
