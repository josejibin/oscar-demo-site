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

Product = get_model('catalogue', 'Product')

Selector = get_class('partner.strategy', 'Selector')


class MyProductLinkSerializer(product.ProductLinkSerializer):
    img_url = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()

    class Meta(product.ProductLinkSerializer.Meta):
        fields = ('url', 'id', 'title', 'images', 'price')

    def get_price(self, obj):
        request = self.context.get("request")
        strategy = Selector().strategy(
            request=request, user=request.user)

        ser = checkout.PriceSerializer(
            strategy.fetch_for_product(obj).price,
            context={'request': request})

        return ser.data

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images


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

    sub_categories = SubCategorySerializer(
        many=True, source='get_children'
    )

    class Meta():
        model = Category
        fields = ('id', 'name', 'img_url', 'sub_categories')

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images


class SubCategoryWithProductSerializer(OscarModelSerializer):
    img_url = serializers.SerializerMethodField()

    products = MyProductLinkSerializer(
        many=True, source='product_set'
    )

    class Meta():
        model = Category
        fields = ('id', 'name', 'img_url', 'products')

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images



class ParentProductSerializer(product.ProductLinkSerializer):

    products = MyProductLinkSerializer(
        many=True, source='children'
    )


    class Meta(product.ProductLinkSerializer.Meta):
        fields = ('url', 'id', 'title', 'images', 'products')

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images


class SubCategorySerializer1(OscarModelSerializer):
    img_url = serializers.SerializerMethodField()

    sub_categories = ParentProductSerializer(
        many=True, source='product_set'
    )

    class Meta():
        model = Category
        fields = ('id', 'name', 'img_url', 'sub_categories')

    def get_img_url(self, obj):
        if not obj.image:
            return ""
        return obj.images
