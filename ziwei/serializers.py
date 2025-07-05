from rest_framework import serializers
from .models import NatalChart, NumerologyAnalysis
from user.models import User


class NatalChartSerializer(serializers.HyperlinkedModelSerializer):
    """用户命盘序列化器"""
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='user:user-detail',
        lookup_field='pk'
    )

    class Meta:
        model = NatalChart
        fields = [
            'url', 'id', 'user', 'year_ganzhi', 'month_ganzhi', 'day_ganzhi',
            'hour_ganzhi', 'wuxing_bureau', 'life_palace', 'body_palace',
            'major_pos', 'aux_pos', 'four_trans', 'patterns', 'wuxing_analysis',
            'calculated_at'
        ]


class NumerologyAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    """数字能量分析序列化器"""
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='user:user-detail',
        lookup_field='pk'
    )

    class Meta:
        model = NumerologyAnalysis
        fields = [
            'url', 'id', 'user', 'life_number', 'digital_patterns', 'analyzed_at'
        ]