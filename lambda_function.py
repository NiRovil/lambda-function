from boto3 import Session
from PIL import Image

import boto3

ACESS_KEY = ''
SECRET_KEY = ''

# acessa a sessão da aws
session = Session(aws_access_key_id=ACESS_KEY, aws_secret_access_key=SECRET_KEY)

def lambda_handler(event, context):

    # acessa os buckets
    s3 = session.resource('s3')
    bucket = s3.Bucket('conversor-imagem')

    # busca todos os items dentro do bucket
    s3_file_key = [s3_file.key for s3_file in bucket.objects.all()]
    names = [s3_file.key[:-4] for s3_file in bucket.objects.all()]

    for key in s3_file_key:

        # busca o objeto e processa na memória, sem precisar de download
        object = bucket.Object(key)
        response = object.get()
        file_stream = response['Body']
        img = Image.open(file_stream).convert("L")

        # transforma a imagem em uma arte ascii
        width, height = img.size
        aspect_ratio = height / width
        new_width = 80
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))

        pixels = img.getdata()

        chars = ["*", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
        new_pixels = [chars[pixel // 25] for pixel in pixels]
        new_pixels = "".join(new_pixels)

        new_pixels_count = len(new_pixels)
        ascii_image = [
            new_pixels[index : index + new_width]
            for index in range(0, new_pixels_count, new_width)
        ]
        ascii_image = "\n".join(ascii_image)

        # atribui um nome ao arquivo
        for name in names:
            file_name = f'{name}.txt'

        text = ascii_image.encode("utf-8")

        # deleta a imagem após a conversão
        s3.Object('conversor-imagem', key).delete()

        # faz o upload do arquivo txt para o bucket 'imagem-ascii'
        s3.Bucket('imagem-ascii').put_object(Key=f'{file_name}', Body=text)