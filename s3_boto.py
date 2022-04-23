import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone
from pathlib import Path

acess_key = ''
acess_secret = ''
bucket_name = 'my_bucket'

data_file_folder = Path('/home/brendo/files/files_local/2.txt')
path_folder_local = Path('/home/brendo/files/files_local')  #pasta local dos certificados

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
client_s3 = boto3.client('s3')

file_name_bucket = 'files/2.txt'
obj = list(bucket.objects.filter(Prefix=file_name_bucket))

if(data_file_folder.is_file() and len(obj) > 0):
        print('Existe em ambos!')
        
        #Comparando datas 
        timestamp = os.path.getmtime('/home/brendo/files/files_local/2.txt') 
        fmt = '%d-%m-%Y %H:%M:%S'
        data_local = datetime.fromtimestamp(timestamp).strftime(fmt) #data file local
        print('data local: ' + data_local)

        key = '2.txt'
        summaryDetails = s3.ObjectSummary(bucket_name, file_name_bucket)
        timeFormat = summaryDetails.last_modified
        data_bucket = timeFormat.strftime("%d-%m-%Y %H:%M:%S") #data file no bucket
        print('data bucket: ' + data_bucket)

        'Upload ou Download de arquivos para bucket S3'

        if(data_local > data_bucket):
                
                try:
                        print('Uploading file {}...'.format(key))
                        client_s3.upload_file(os.path.join(path_folder_local, key),bucket_name,key)
                except ClientError as e:
                        print('Credencial está incorreta')
                        print(e)
                except Exception as e:
                        print(e)
        else:
                print('Download file {}...'.format(key))
                client_s3.download_file(bucket_name, key, os.path.join(path_folder_local, '2.txt'))
else:
        print('Não existe.')

