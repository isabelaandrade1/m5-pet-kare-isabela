from rest_framework import serializers
from groups.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "scientific_name", "created_at"]
        read_only_fields = ["id", "created_at"]
