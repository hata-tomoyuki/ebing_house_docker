import os
import django

# settings.pyを明示的に指定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Djangoの設定を初期化
django.setup()

from django.core.mail import send_mail

send_mail(
    'テストメール',
    'これはテストメールです。',
    'hirotrics@gmail.com',  # 送信元
    ['hirotorics@gmail.com'],  # 送信先
    fail_silently=False,
)