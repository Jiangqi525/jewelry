from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    """用户主表（优化出生时间字段）"""
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )

    # 合并为单一 datetime 字段，存储出生时间（精确到时辰）
    birth_datetime = models.DateTimeField('出生时间', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField('手机号', max_length=20, null=True, blank=True)
    wechat_openid = models.CharField('微信OpenID', max_length=128, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息管理'

    def __str__(self):
        return f"{self.username} ({self.get_gender_display()})"

    # 新增属性：从 birth_datetime 解析年月日时
    @property
    def birth_year(self):
        return self.birth_datetime.year if self.birth_datetime else None

    @property
    def birth_month(self):
        return self.birth_datetime.month if self.birth_datetime else None

    @property
    def birth_day(self):
        return self.birth_datetime.day if self.birth_datetime else None

    @property
    def birth_hour(self):
        # 时辰计算：2小时为一个时辰（如0-2点为子时，2-4点为丑时）
        return (self.birth_datetime.hour // 2) + 1 if self.birth_datetime else None


class ClickRecord(models.Model):
    """用户点击记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    jewelry = models.ForeignKey('zhubao.JewelryItem', on_delete=models.CASCADE, verbose_name='珠宝商品')
    clicked_at = models.DateTimeField('点击时间', auto_now_add=True)
    source = models.CharField('来源', max_length=50,
                              choices=[('recommendation', '推荐页面'), ('search', '搜索页面'), ('other', '其他')])
    duration = models.FloatField('停留时长(秒)', default=0.0)
    recommendation = models.ForeignKey('zhubao.Recommendation', on_delete=models.SET_NULL,
                                       null=True, blank=True, verbose_name='关联推荐')

    class Meta:
        verbose_name = '点击记录'
        verbose_name_plural = '用户行为追踪'
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['clicked_at']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return f"{self.user.username}点击{self.jewelry.name} ({self.clicked_at.strftime('%H:%M')})"


class FengShuiSetting(models.Model):
    """用户风水设置"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    tags = models.JSONField('风水标签', default=list,
                            help_text='用户设置的风水标签，如["东南", "土"]')
    home_direction = models.CharField('房屋朝向', max_length=10,
                                      choices=[('north', '北'), ('south', '南'), ('east', '东'), ('west', '西')],
                                      blank=True)
    last_updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '风水设置'
        verbose_name_plural = '风水偏好管理'

    def __str__(self):
        return f"{self.user.username}的风水设置"