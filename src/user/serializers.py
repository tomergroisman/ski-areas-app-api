from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from core.services.translation import i18n


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a user"""
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    email = serializers.CharField(required=False)

    def validate(self, data):
        """Validate and authenticate the user"""
        username = data.get('username')
        password = data.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = i18n('AUTH_INVALID_CREDENTIALS')
            raise serializers.ValidationError(msg, code='authentication')

        data['user'] = user
        return data
