from oscar.core.loading import get_class, get_model
from rest_framework import generics
from rest_framework.response import Response

from oscarapi import serializers
from oscarapi.views import product

from .serializers import MyCategorySerializer, MyProductLinkSerializer


class ProductList(product.ProductList):
    serializer_class = MyProductLinkSerializer




Category = get_model('catalogue', 'category')


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = MyCategorySerializer

    def get_queryset(self):
        """
        Allow filtering on structure so standalone and parent products can
        be selected separately, eg::
            http://127.0.0.1:8000/api/products/?structure=standalone
        or::
            http://127.0.0.1:8000/api/products/?structure=parent
        """
        qs = super(CategoryList, self).get_queryset()
        return qs
