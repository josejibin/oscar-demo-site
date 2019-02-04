from oscar.core.loading import get_class

from rest_framework import serializers
from oscar.core.loading import get_class, get_model
from oscarapi.serializers import checkout, product

from oscarapi.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)

Category = get_model('catalogue', 'category')


Selector = get_class('partner.strategy', 'Selector')


class MyProductLinkSerializer(product.ProductLinkSerializer):
    images = serializers.SerializerMethodField('get_alternate_name')
    price = serializers.SerializerMethodField()

    class Meta(product.ProductLinkSerializer.Meta):
        fields = ('url', 'id', 'title', 'images', 'price', 'country_code')

    def get_price(self, obj):
        request = self.context.get("request")
        strategy = Selector().strategy(
            request=request, user=request.user)

        ser = checkout.PriceSerializer(
            strategy.fetch_for_product(obj).price,
            context={'request': request})

        return ser.data

    def get_alternate_name(self, obj):
        return "jibinjose"


class SubCategorySerializer(OscarModelSerializer):
    images = serializers.SerializerMethodField('get_alternate_name')

    class Meta():
        model = Category
        fields = ('id', 'name', 'images', 'country_code')

    def get_alternate_name(self, obj):
        return "jibinjose"


class MyCategorySerializer(OscarModelSerializer):
    images = serializers.SerializerMethodField('get_alternate_name')

    sub_categories = SubCategorySerializer(many=True, source='get_children')

    class Meta():
        model = Category
        fields = ('id', 'name', 'images', 'country_code', 'sub_categories')

    def get_alternate_name(self, obj):
        return "jibinjose"

