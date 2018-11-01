# -*- coding: utf-8 -*-
import os
import tensorflow as tf

from google.colab import auth
from googleapiclient import discovery, http

from pathlib import Path

"""## GCP Auth"""

bucket_name = '' #@param {type:"string"}
assert bucket_name, 'Must specify an existing GCS bucket name'
print('Using bucket: {}'.format(bucket_name))

auth.authenticate_user()

"""## Download dataset"""

origin_url = 'https://people.eecs.berkeley.edu/~tinghuiz/projects/pix2pix/datasets/facades.tar.gz'
path_to_zip = tf.keras.utils.get_file('facades.tar.gz',
                                                                cache_subdir=os.path.abspath('.'),
                                                                origin=origin_url,
                                                                extract=True)

data_path = Path(path_to_zip).parent.joinpath('facades')
for i in ['train', 'val', 'test']:
  print(i, len(list(data_path.joinpath(i).glob('*.jpg'))))

"""## Upload to gcs"""

def create_service():
  return discovery.build('storage', 'v1')

def upload_objects(bucket, paths):
  service = create_service()

  for path in paths:

    body = {
        'name': 'data/' + '/'.join(str(path).split('/')[3:]),
    }

    with open(path, 'rb') as f:
      req = service.objects().insert(bucket=bucket,
                                                          body=body,
                                                          media_body=http.MediaIoBaseUpload(f, 'application/octet-stream'))

      resp = req.execute()

upload_objects(bucket_name, data_path.glob('*/*.jpg'))
