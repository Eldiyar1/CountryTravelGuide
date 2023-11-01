import hashlib


def calculate_file_hash(file):
    file_hash = hashlib.md5()
    for chunk in file.chunks():
        file_hash.update(chunk)
    return file_hash.hexdigest()
