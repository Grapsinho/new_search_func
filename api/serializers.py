from rest_framework import serializers
from inventory.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description"]

class mediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["image"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_url = representation['image']

        # Split the image URL by '/' and keep only the path after 'images/'
        path_parts = image_url.split('/images/')
        if len(path_parts) > 1:
            representation['image'] = path_parts[1]

        return representation

class ProductInventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)  # Including the ProductSerializer as a nested serializer
    media_product_inventory = mediaSerializer(many=True, read_only=True)
    # brand = BrandSerializer()
    # product_type = ProductTypeSerializer()
    # #SerializerMethodField ეს გვჭირდება რათა განვსაზღვროთ მეთოდები ამისთვის
    # #როდესაც მეთოდს ვწერთ და გვინდა რომ კონკრეტულად ამისთვის იყოს მაშ სახელეს წინ get უნდა დავუწეროთ
    # attribute_values = serializers.SerializerMethodField()


    class Meta:
        model = ProductInventory
        fields = ["id", "retail_price", "product", "media_product_inventory"]
    
    # def get_attribute_values(self, obj):
    #     return list(obj.attribute_values.values_list('attribute_value', flat=True))