import hashlib


def calculate_file_hash(file):
    file_hash = hashlib.md5()
    for chunk in file.chunks():
        file_hash.update(chunk)
    return file_hash.hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
