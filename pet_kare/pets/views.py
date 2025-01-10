from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from pets.models import Pet
from pets.serializers import PetSerializer
from groups.models import Group
from traits.models import Trait

class PetPagination(PageNumberPagination):
    page_size = 2  # Retorna 2 pets por página

class PetListCreateView(ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    pagination_class = PetPagination

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
