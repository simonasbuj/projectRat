from uuid import uuid4
import os

def book_cover_upload(instance, filename):
    upload_to = 'books'
    ext = filename.split('.')[-1]
    original_file_name = filename.split('.')[0]

    filename = '{}{}.{}'.format(instance.title, uuid4().hex, ext) #instance.last_name, original_file_name

    # return the whole path to the file
    return os.path.join(upload_to, filename)

