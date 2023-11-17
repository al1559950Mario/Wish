from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import Categories, Products, Recommendations
from rest_framework import viewsets
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .serializers import RecommendationSerializer
from django.http import HttpResponse

# Categorías
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

# Productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

# Recomendaciones
class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationSerializer
