from rest_framework import serializers
from fastuser import models
#
# 在定义的时候，指定了一些参数，这里只用了read_only，另外还有write_only,required,allow_null/allow_blank,label,help_text,style，error_messages
# read_only：表示该字段只能用于API的输出，用户并不能直接指定该字段的值
# write_only：这个就和read_only相反，需要用户指定该字段的值
# required：该字段是必需的，不能为空
# allow_null/allow_blank：该字段允许为null/空
# label：标签，用于对字段显示设置
# help_text：对字段进行解释的一段文本，用于提示
# style：说明字段的类型
# error_messages：字段出错时，信息提示


class UserInfoSerializer(serializers.Serializer):
    """
    用户信息序列化
    建议实现其他方法，否则会有警告
    """
    username = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "用户名校验失败"
    })

    password = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "密码校验失败"
    })

    email = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "邮箱校验失败"
    })

    def create(self, validated_data):
        """
        实现create方法
        """
        return models.UserInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
