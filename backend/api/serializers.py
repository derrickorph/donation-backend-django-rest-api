from rest_framework import serializers

from api.models import User, IdentificationNumber, Donation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "surname", "is_superuser", 'is_active', "id_number", "nationality", "email", "bank", "acc",
                  "phoneNumber", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class IdentificationNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationNumber
        fields = ["id", "number", 'created_at']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class DonationSerializer(serializers.ModelSerializer):
    user_relation = UserSerializer(many=False, source='user', read_only=True)
    donator_relation = UserSerializer(many=False, source='donator', read_only=True)

    class Meta:
        model = Donation
        fields = ["id", "status", 'user', "donator", 'amount', 'created_at', 'user_relation', 'donator_relation']
        extra_kwargs = {
            'user': {'read_only': True},
            'donator': {'read_only': True},
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
