from django.db import models
from user.models import User

class NatalChart(models.Model):
    """用户命盘表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    year_ganzhi = models.CharField('年干支', max_length=20)
    month_ganzhi = models.CharField('月干支', max_length=20)
    day_ganzhi = models.CharField('日干支', max_length=20)
    hour_ganzhi = models.CharField('时干支', max_length=20)
    wuxing_bureau = models.CharField('五行局', max_length=50)
    life_palace = models.CharField('命宫', max_length=20)
    body_palace = models.CharField('身宫', max_length=20)
    major_pos = models.JSONField('主星位置', default=dict,
                               help_text='主星分布字典，格式: {"紫微": 1, "天机": 2}')
    aux_pos = models.JSONField('辅星位置', default=dict,
                             help_text='辅星分布字典，格式: {"文昌": 3, "文曲": 4}')
    four_trans = models.JSONField('四化星', default=dict,
                                help_text='四化星信息，格式: {"年干禄": "廉贞"}')
    patterns = models.JSONField('格局分析', default=list,
                              help_text='识别到的格局列表，格式: [{"name": "紫府朝垣", ...}]')
    wuxing_analysis = models.JSONField('五行分析', default=dict,
                                     help_text='五行平衡分析结果')
    calculated_at = models.DateTimeField('计算时间', auto_now_add=True)

    class Meta:
        verbose_name = '命盘信息'
        verbose_name_plural = '用户命盘管理'
        unique_together = [('user', 'calculated_at')]

    def __str__(self):
        return f"{self.user.username}的命盘 ({self.calculated_at.strftime('%Y-%m-%d')})"

class NumerologyAnalysis(models.Model):
    """数字能量分析表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    life_number = models.IntegerField('生命数字')
    digital_patterns = models.JSONField('数字磁场模式', default=list,
                                      help_text='识别到的数字磁场列表')
    analyzed_at = models.DateTimeField('分析时间', auto_now_add=True)

    class Meta:
        verbose_name = '数字能量分析'
        verbose_name_plural = '数字能量管理'

    def __str__(self):
        return f"{self.user.username}的数字能量分析"