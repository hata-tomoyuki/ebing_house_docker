from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from wlist.models import MemoModel

from datetime import datetime

class Memo1Serializer(serializers.ModelSerializer):
    # reg_date = serializers.DateField() 
    reg_date = serializers.DateField(required=False, allow_null=True)
    class Meta:
        model = MemoModel
        fields = ('id','user','memo','reg_date')
        extra_kwargs = {'user':{ 'read_only':True}}
        
    def create(self, validated_data):
        # リクエストのuserを取得
        user = self.context['request'].user
        return MemoModel.objects.create(user=user, **validated_data)

# 特定のフィールドのバリデーションが行われる際に自動的に呼び出されます。
    # def validate_reg_date(self, value):
    #     if isinstance(value, datetime):
    #         return value.date()  # datetimeをdateに変換
    #     return value

# class MemoModel(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     memo = models.TextField()
#     reg_date = models.DateField(blank=True,null=True)
           
#     def __str__(self):
#         if len(self.memo) > 50:
#             return self.memo[:50]
#         else:
#             return self.memo
    
#     def save(self, *args, **kwargs):
#         user1 = kwargs.pop('user', None)
#         if user1:
#             self.user = user1
        
#         if not self.pk:
#             self.reg_date = timezone.now()    
#         else:  # 更新時
#             original = MemoModel.objects.get(pk=self.pk)
#             self.user = original.user
#             self.reg_date = original.reg_date

#         super(MemoModel, self).save(*args, **kwargs)