import os
from openai import OpenAI
from batch.unused.batch_mysql_test import get_target_mysql

# .envファイルの読み込み (dotenvが必要なら以下を追加)
from dotenv import load_dotenv

load_dotenv()

# 出力フォルダとファイル名
output_folder = "media/images2"

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

tbl = os.getenv('BATCH_CHECK_TABLE')
print(tbl)
username="12"
word_list = get_target_mysql(tbl,username)

# for i in range(len(word_list)):
for i in range(5):
  # 多様なイメージが抱かれる場合は、各イメージが１枚の画像に含まれるようにしてください。
  
  prompt_template = os.getenv('WORD_PROMPT')
  prompt = prompt_template.format(word=word_list[i])

  output_filename = f"{word_list[i]}.webp"
  print(prompt)
  
  client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

  try:
    # OpenAI APIを使用して画像を生成
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    
    # 画像をダウンロードして保存
    import requests
    img_data = requests.get(image_url).content
    with open(os.path.join(output_folder, output_filename), 'wb') as handler:
        handler.write(img_data)
    
    print(f"画像が正常に保存されました: {os.path.join(output_folder, output_filename)}")

  except Exception as e:
    print(f"エラーが発生しました: {e}")
