from uuid import uuid4
import os

def user_avatar_upload(instance, filename):
    upload_to = 'users/'
    ext = filename.split('.')[-1]
    original_file_name = filename.split('.')[0]

    filename = '{}/{}.{}'.format(instance.user.username, original_file_name, ext) #instance.last_name, original_file_name

    # return the whole path to the file
    return os.path.join(upload_to, filename)

