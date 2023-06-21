from urllib.parse import urlparse
import requests

def get_attachment_name(url):
    path = urlparse(url).path
    position = path.rfind('/') + 1
    length = len(path)
    name = path[position:length]
    return name

def download_attachment(url, path):
    name = get_attachment_name(url)
    p = path + name
    r = requests.get(url)
    open(p, 'wb').write(r.content)
