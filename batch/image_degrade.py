from PIL import Image
import os

def resize_and_compress_image(input_path, output_path, new_size=(512, 512), quality=85):
    """
    画像をリサイズして圧縮する
    """
    with Image.open(input_path) as img:
        img = img.resize(new_size, Image.LANCZOS)  # リサイズ
        img.save(output_path, format='WEBP', optimize=True, quality=quality)


def __main__():
    folder_path = 'media/images'
    output_folder = 'media/compressed_images'  # 圧縮後の画像を保存するフォルダ
    os.makedirs(output_folder, exist_ok=True)

    # フォルダ内のwebpファイルを処理
    for filename in os.listdir(folder_path):
        if filename.endswith('.webp'):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            resize_and_compress_image(input_path, output_path)
            print(f'{filename} has been resized and compressed.')

    print(f"Compressed images saved in '{output_folder}' folder.")
