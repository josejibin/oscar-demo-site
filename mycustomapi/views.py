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
    queryset = Category.objects.filter()
    serializer_class = MyCategorySerializer

    def get_queryset(self):
        """
        """
        qs = super(CategoryList, self).get_queryset()
        qs = qs.filter(depth__in=[0, 1])
        return qs
