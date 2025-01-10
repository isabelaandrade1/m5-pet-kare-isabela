from django.urls import path
from pets.views import (
    PetListCreateView,
    PetDetailView
)

urlpatterns = [
    path('', PetListCreateView.as_view(), name='pets-list-create'),  # Listar e criar pets
    path('<int:pet_id>/', PetDetailView.as_view(), name='pet-detail'),  # Operações por ID
]
