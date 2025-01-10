from rest_framework import serializers
from pets.models import Pet
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from groups.models import Group
from traits.models import Trait

class PetSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "age", "weight", "sex", "group", "traits"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        group, _ = Group.objects.get_or_create(**group_data)
        pet = Pet.objects.create(**validated_data, group=group)

        for trait_data in traits_data:
            trait, _ = Trait.objects.get_or_create(**trait_data)
            pet.traits.add(trait)

        return pet
