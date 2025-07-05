from rest_framework import serializers
from .models import JewelryCategory, JewelryItem, Recommendation
from user.models import User
from ziwei.models import NatalChart


class JewelryCategorySerializer(serializers.HyperlinkedModelSerializer):
    """珠宝分类序列化器（处理自关联）"""
    parent = serializers.HyperlinkedRelatedField(
        queryset=JewelryCategory.objects.all(),
        view_name='zhubao:jewelrycategory-detail',
        lookup_field='pk',
        required=False
    )

    class Meta:
        model = JewelryCategory
        fields = ['url', 'id', 'name', 'description', 'parent', 'created_at']


class JewelryItemSerializer(serializers.HyperlinkedModelSerializer):
    """珠宝商品序列化器"""
    category = serializers.HyperlinkedRelatedField(
        queryset=JewelryCategory.objects.all(),
        view_name='zhubao:jewelrycategory-detail',
        lookup_field='pk',
        required=False
    )

    class Meta:
        model = JewelryItem
        fields = [
            'url', 'id', 'name', 'category', 'wuxing', 'price_tier',
            'description', 'image_url', 'digital_tags', 'fengshui_tags',
            'base_price', 'is_active', 'created_at', 'updated_at'
        ]


class RecommendationSerializer(serializers.HyperlinkedModelSerializer):
    """珠宝推荐记录序列化器"""
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='user:user-detail',
        lookup_field='pk'
    )
    natal_chart = serializers.HyperlinkedRelatedField(
        queryset=NatalChart.objects.all(),
        view_name='ziwei:natalchart-detail',
        lookup_field='pk',
        required=False
    )
    jewelry_items = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=JewelryItem.objects.all(),
        view_name='zhubao:jewelryitem-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Recommendation
        fields = [
            'url', 'id', 'user', 'recommend_type', 'fee', 'jewelry_items',
            'natal_chart', 'reason', 'recommended_at', 'is_viewed', 'conversion_rate'
        ]