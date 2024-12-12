from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import deepl

from dotenv import load_dotenv
import os

load_dotenv()

# from django.contrib.auth.models import AbstractUser

# Create your models here.

class WordsModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    word = models.CharField(max_length=20)
    mean1 = models.CharField(max_length=15,blank=True,null=True)
    mean2 = models.CharField(max_length=200,blank=True,null=True)
    reg_date = models.DateField(default=timezone.now, blank=True,null=True)
    
    ## 追加
    fusen = models.BooleanField(default=False)
    img = models.ImageField(upload_to='images/', default='images/default.webp', null=True, blank=True)
    
    def __str__(self):
        return self.word
    
    def save(self, *args, **kwargs):
        user1 = kwargs.pop('user', None)
        if user1:
            self.user = user1
        
        # if not self.pk:
        #     self.reg_date = timezone.now()
        if not self.pk:
            self.mean1 = self.api_meanings(self.word)
            self.mean2 = self.scrape_meanings(self.word)
            if len(self.mean1) > 15:
                raise ValidationError({'mean1': 'mean1 must be smaller than 15'})
            if len(self.mean2) > 200:
                raise ValidationError({'mean2': 'mean2 must be smaller than 200'})
            
        else:  # 更新時
            original = WordsModel.objects.get(pk=self.pk)
            self.user = original.user
            self.reg_date = original.reg_date

        super(WordsModel, self).save(*args, **kwargs)
        
    def scrape_meanings(self, phrase):
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
    
    def api_meanings(self,phrase):

        auth_key = os.getenv('DEEPL_SECRET_KEY')
        try:
            translator = deepl.Translator(auth_key)
            result = translator.translate_text(phrase, target_lang="JA")
            print(result.text)
            return result.text
        except Exception as e:
            return "not get"

    
class MemoModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    memo = models.TextField()
    # reg_date = models.DateField(blank=True,null=True)
    reg_date = models.DateField(default=timezone.now, blank=True, null=True)

           
    def __str__(self):
        if len(self.memo) > 50:
            return self.memo[:50]
        else:
            return self.memo
    
    def save(self, *args, **kwargs):
        user1 = kwargs.pop('user', None)
        if user1:
            self.user = user1
        
        # if not self.pk:
        #     self.reg_date = timezone.now().date() 

        if self.pk:
            original = MemoModel.objects.get(pk=self.pk)
            self.user = original.user
            self.reg_date = original.reg_date

        super(MemoModel, self).save(*args, **kwargs)
        
        
class McModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    memo1 = models.CharField(max_length=50)    
    memo2 = models.TextField(blank=True,null=True)
    reg_date = models.DateField(default=timezone.now,blank=True,null=True)
           
    def __str__(self):
        if len(self.memo1) > 50:
            return self.memo1[:50]
        else:
            return self.memo1
    
    def save(self, *args, **kwargs):
        user1 = kwargs.pop('user', None)
        if user1:
            self.user = user1
        
        # if not self.pk:
        #     self.reg_date = timezone.now()    
        # else:  # 更新時
        
        if self.pk:
            original = McModel.objects.get(pk=self.pk)
            self.user = original.user
            self.reg_date = original.reg_date

        super(McModel, self).save(*args, **kwargs)