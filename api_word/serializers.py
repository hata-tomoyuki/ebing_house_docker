from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from wlist.models import WordsModel

from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import deepl
from dotenv import load_dotenv
import os

load_dotenv()


class WordsSerializer(serializers.ModelSerializer):
    mean1 = serializers.CharField(required=False)
    mean2 = serializers.CharField(required=False)
    reg_date = serializers.DateField(required=False, allow_null=True)
    fusen = serializers.BooleanField(required=False,default=False)
    img = serializers.ImageField(required=False, default='images/default.webp', allow_null=True)

    class Meta:
        model = WordsModel
        fields = ('id','user','word','mean1','mean2','reg_date','fusen','img')
        # extra_kwargs = {'user':{ 'read_only':True}}
    
    def create(self, validated_data):
        # `mean1` と `mean2` を自動生成
        word = validated_data.get('word')
        validated_data['mean1'] = self.generate_mean1(word)
        validated_data['mean2'] = self.generate_mean2(word)
        validated_data['reg_date'] = timezone.now().date()
        validated_data['fusen'] = False
        validated_data['img'] = 'images/default.webp'
        
        
        
        # 他のバリデーションやユーザーの設定
        validated_data['user'] = self.context['request'].user

        return WordsModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # `mean1` や `mean2` の手動修正を許可
        instance.mean1 = validated_data.get('mean1', instance.mean1)
        instance.mean2 = validated_data.get('mean2', instance.mean2)
        instance.word = validated_data.get('word', instance.word)
        # instance.fusen = validated_data.get('fusen', instance.fusen)
        # instance.img = validated_data.get('img', instance.img)

        instance.save()
        return instance

    def generate_mean1(self, word):
        auth_key = os.getenv('DEEPL_SECRET_KEY')
        try:
            translator = deepl.Translator(auth_key)
            result = translator.translate_text(phrase, target_lang="JA")
            print(result.text)
            return result.text
        except Exception as e:
            return "not get"

    def generate_mean2(self, phrase):
        url = f"https://ejje.weblio.jp/content/{phrase}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'twitter:description'})
        if meta_tag:
            content = meta_tag.get('content')
            try:
                meaning = content.split(': ')[1]
                return meaning
            except:
                return "-----------------------------"
        return None    

    # def create(self, validated_data):
    #     # リクエストのuserを取得
    #     user = self.context['request'].user
    #     return WordsModel.objects.create(user=user, **validated_data)

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