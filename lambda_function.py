from boto3 import Session

import pywhatkit
import boto3
import glob, os

def lambda_handler(event, context):

    name = ''
    directory = os.getcwd()

    ACESS_KEY = ''
    SECRET_KEY = ''

    session = Session(aws_access_key_id=ACESS_KEY, aws_secret_access_key=SECRET_KEY)

    s3 = session.resource('s3')
    conversor_imagem = s3.Bucket('conversor-imagem')

    for s3_file in conversor_imagem.objects.all():
        name = s3_file.key[:-4]

    s3 = boto3.client('s3')

    s3.download_file('conversor-imagem', s3_file.key, f'{directory}./imagem.png')

    images = [file for file in glob.glob(f'{directory}/*.png')]
    print(images)

    for image in images:
        txt_file = pywhatkit.image_to_ascii_art(image, name)
        print(txt_file)

    s3.upload_file(name+'.txt', 'imagem-ascii', name+'.txt')