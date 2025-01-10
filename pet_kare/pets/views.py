from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from pets.models import Pet
from pets.serializers import PetSerializer
from groups.models import Group
from traits.models import Trait

# Paginação personalizada
class PetPagination(PageNumberPagination):
    page_size = 2  # Retorna 2 pets por página

# Listagem e criação de pets
class PetListCreateView(ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    pagination_class = PetPagination

    def get_queryset(self):
        # Filtrar por trait (query param)
        trait_name = self.request.query_params.get('trait')
        if trait_name:
            return Pet.objects.filter(traits__name__iexact=trait_name)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        data = request.data

        # Verificar ou criar grupo
        group_data = data.get('group')
        group, _ = Group.objects.get_or_create(**group_data)

        # Verificar ou criar traits
        traits_data = data.get('traits')
        traits = []
        for trait_data in traits_data:
            trait_name = trait_data['trait_name'].lower()
            trait, _ = Trait.objects.get_or_create(name__iexact=trait_name, defaults={'name': trait_name})
            traits.append(trait)

        # Criar pet
        pet_data = {key: value for key, value in data.items() if key not in ['group', 'traits']}
        pet = Pet.objects.create(**pet_data, group=group)
        pet.traits.set(traits)

        # Serializar e retornar resposta
        serializer = self.get_serializer(pet)
        return Response(serializer.data, status=201)

# Operações detalhadas (GET, PATCH, DELETE)
class PetDetailView(APIView):
    def get(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def patch(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        data = request.data

        # Atualizar grupo, se fornecido
        if 'group' in data:
            group_data = data.pop('group')
            group, _ = Group.objects.get_or_create(**group_data)
            pet.group = group

        # Atualizar traits, se fornecido
        if 'traits' in data:
            traits_data = data.pop('traits')
            traits = []
            for trait_data in traits_data:
                trait_name = trait_data['trait_name'].lower()
                trait, _ = Trait.objects.get_or_create(name__iexact=trait_name, defaults={'name': trait_name})
                traits.append(trait)
            pet.traits.set(traits)

        # Atualizar demais campos
        for attr, value in data.items():
            setattr(pet, attr, value)
        pet.save()

        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
