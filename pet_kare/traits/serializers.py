from rest_framework import serializers
from traits.models import Trait

class TraitSerializer(serializers.ModelSerializer):
    trait_name = serializers.CharField(source="name")

    class Meta:
        model = Trait
        fields = ["id", "trait_name", "created_at"]
        read_only_fields = ["id", "created_at"]
