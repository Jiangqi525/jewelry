from django.db import models


class JewelryCategory(models.Model):
    """珠宝分类表"""
    name = models.CharField('分类名称', max_length=50)
    description = models.TextField('分类描述', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='父级分类')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '珠宝分类'
        verbose_name_plural = '珠宝分类管理'
        db_table = 'jewelry_category'

    def __str__(self):
        return self.name


class JewelryItem(models.Model):
    """珠宝商品表"""
    PRICE_TIER_CHOICES = (
        ('high', '高端'),
        ('mid', '中端'),
        ('low', '入门'),
    )

    name = models.CharField('珠宝名称', max_length=255)
    category = models.ForeignKey(JewelryCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='所属分类')
    wuxing = models.CharField('五行属性', max_length=10,
                              choices=[('金', '金'), ('木', '木'), ('水', '水'), ('火', '火'), ('土', '土')])
    price_tier = models.CharField('价格等级', max_length=10, choices=PRICE_TIER_CHOICES)
    description = models.TextField('详细描述', blank=True)
    image_url = models.URLField('图片链接', max_length=500, blank=True)
    digital_tags = models.JSONField('数字标签', default=list,
                                    help_text='存储数字磁场的标签列表，如[3, 9, "天医"]')
    fengshui_tags = models.JSONField('风水标签', default=list,
                                     help_text='存储风水属性的标签列表，如["东南", "土"]')
    base_price = models.DecimalField('基础价格', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('是否上架', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '珠宝商品'
        verbose_name_plural = '珠宝商品管理'
        indexes = [
            models.Index(fields=['wuxing']),
            models.Index(fields=['price_tier']),
        ]
        db_table = 'jewelry_item'

    def __str__(self):
        return f"{self.name} ({self.get_wuxing_display()})"


class Recommendation(models.Model):
    """珠宝推荐记录"""
    RECOMMEND_TYPE_CHOICES = (
        ('year_recommend', '年度五行推荐'),
        ('month_day_recommend', '月日数字推荐'),
        ('fengshui_recommend', '风水环境推荐'),
        ('click_based', '点击行为推荐'),
        ('ai_suggest', 'AI个性推荐'),
    )

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='所属用户')
    recommend_type = models.CharField('推荐类型', max_length=20, choices=RECOMMEND_TYPE_CHOICES)
    fee = models.DecimalField('服务费用', max_digits=10, decimal_places=2, default=0.0)
    jewelry_items = models.ManyToManyField(JewelryItem, verbose_name='推荐珠宝')
    natal_chart = models.ForeignKey('ziwei.NatalChart', on_delete=models.SET_NULL,
                                    null=True, blank=True, verbose_name='关联命盘')
    reason = models.TextField('推荐理由', blank=True)
    recommended_at = models.DateTimeField('推荐时间', auto_now_add=True)
    is_viewed = models.BooleanField('用户已查看', default=False)
    conversion_rate = models.FloatField('转化率', default=0.0,
                                        help_text='用户点击推荐商品的比例')

    class Meta:
        verbose_name = '推荐记录'
        verbose_name_plural = '珠宝推荐管理'
        ordering = ['-recommended_at']
        indexes = [
            models.Index(fields=['recommend_type']),
            models.Index(fields=['is_viewed']),
        ]
        db_table = 'jewelry_recommend'

    def __str__(self):
        return f"{self.user.username}的{self.get_recommend_type_display()} ({self.recommended_at.strftime('%Y-%m-%d')})"