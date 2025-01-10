from django.urls import path
from pets.views import PetListCreateView

urlpatterns = [
    path('', PetListCreateView.as_view(), name='pets-list-create'),  
]
