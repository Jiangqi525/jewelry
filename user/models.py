from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from jewellery.models import JewelryItem, Recommendation


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

    # 解决反向访问器冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='所属组',
        related_name='custom_user_set',  # 添加唯一的related_name
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='用户权限',
        related_name='custom_user_permissions_set',  # 添加唯一的related_name
        blank=True,
    )


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息管理'
        db_table = 'user'

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
        user = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='用户')
        jewelry = models.ForeignKey(
            JewelryItem,  # 直接引用模型类
            on_delete=models.CASCADE,
            verbose_name='点击的珠宝',
            blank=True,
            null=True,
        )
        recommendation = models.ForeignKey(
            Recommendation,  # 直接引用模型类
            on_delete=models.CASCADE,
            verbose_name='关联推荐',
            blank=True,
            null=True,
        )
        click_time = models.DateTimeField('点击时间', auto_now_add=True)
        ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)

        class Meta:
            verbose_name = '用户点击记录'
            verbose_name_plural = '用户点击记录管理'
            ordering = ['-click_time']
            db_table = 'user_click_record'

        def __str__(self):
            return f"{self.user.username}点击了{self.jewelry.name if self.jewelry else '未知珠宝'}"

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
        db_table = 'fengshui_setting'

    def __str__(self):
        return f"{self.user.username}的风水设置"