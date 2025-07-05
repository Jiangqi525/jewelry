from rest_framework import serializers
from .models import User, ClickRecord, FengShuiSetting
from jewellery.models import JewelryItem
from jewellery.serializers import JewelryItemSerializer
from ziwei.models import NatalChart
from rest_framework.exceptions import ValidationError
import datetime


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """用户信息序列化器（处理出生时间合并字段）"""
    # 只读属性：从birth_datetime自动解析
    birth_year = serializers.IntegerField(read_only=True)
    birth_month = serializers.IntegerField(read_only=True)
    birth_day = serializers.IntegerField(read_only=True)
    birth_hour = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url', 'id', 'username', 'email', 'birth_datetime',
            'birth_year', 'birth_month', 'birth_day', 'birth_hour',
            'gender', 'phone', 'wechat_openid', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # 密码只写
            'birth_datetime': {
                'help_text': '格式示例：2000-01-01 12:00（支持YYYY-MM-DD HH:MM格式）'
            }
        }

    def validate_birth_datetime(self, value):
        """验证出生时间的合理性"""
        if value:
            # 检查是否早于1900年或晚于当前时间
            if value < datetime.datetime(1900, 1, 1) or value > datetime.datetime.now():
                raise ValidationError("出生时间需在1900年至今范围内")
        return value


class ClickRecordSerializer(serializers.HyperlinkedModelSerializer):
    """用户点击记录序列化器"""
    jewelry = serializers.HyperlinkedRelatedField(
        queryset=JewelryItem.objects.all(),
        view_name='zhubao:jewelryitem-detail',
        lookup_field='pk'
    )
    # 可选：嵌套珠宝详情（如需展示珠宝完整信息）
    jewelry_detail = JewelryItemSerializer(source='jewelry', read_only=True)
    recommendation = serializers.HyperlinkedRelatedField(
        queryset=NatalChart.objects.all(),
        view_name='ziwei:natalchart-detail',
        lookup_field='pk',
        required=False
    )

    class Meta:
        model = ClickRecord
        fields = [
            'url', 'id', 'user', 'jewelry', 'jewelry_detail', 'clicked_at',
            'source', 'duration', 'recommendation'
        ]


class FengShuiSettingSerializer(serializers.HyperlinkedModelSerializer):
    """用户风水设置序列化器"""

    class Meta:
        model = FengShuiSetting
        fields = [
            'url', 'id', 'user', 'tags', 'home_direction', 'last_updated'
        ]