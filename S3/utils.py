from urllib.parse import urlparse, unquote


def parseurl(url:str) -> list:
    parse_url = urlparse(url)
    clean_path = unquote(parse_url.path)
    path = clean_path.strip("/").split("/", 1)

    return path