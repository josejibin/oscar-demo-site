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
    img_url = serializers.SerializerMethodField()

    class Meta():
        model = Category
        fields = ('id', 'name', 'img_url')

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images


class MyCategorySerializer(OscarModelSerializer):
    img_url = serializers.SerializerMethodField()

    sub_categories = SubCategorySerializer(many=True, source='get_children')

    class Meta():
        model = Category
        fields = ('id', 'name', 'img_url', 'sub_categories')

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images

