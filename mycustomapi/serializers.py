from oscar.core.loading import get_class

from rest_framework import serializers

from oscarapi.serializers import checkout, product


Selector = get_class('partner.strategy', 'Selector')


class MyProductLinkSerializer(product.ProductLinkSerializer):
    images = serializers.SerializerMethodField('get_alternate_name')
    price = serializers.SerializerMethodField()
    country_code = serializers.CharField(source='id')

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
