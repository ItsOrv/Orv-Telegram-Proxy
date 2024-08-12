# utils.py
# shared helpers (work in progress)

import re


def extract_proxy_params(link):
    server = re.search(r'server=([^&]+)', link)
    port = re.search(r'port=([^&]+)', link)
    if not server or not port:
        return None
    return server.group(1), port.group(1)


def shorten_ip(ip, limit=16):
    if len(ip) > limit:
        return ip[:limit] + '.etc'
    return ip
