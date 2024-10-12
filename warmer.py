from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import time
import requests
import xml.etree.ElementTree as ET


def main(url):
    print("Loading %s" % url)
    response = requests.get(url)
    xml_content = response.content
    
    root = ET.fromstring(xml_content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    links = []
    for url in root.findall('ns:url/ns:loc', namespace):
        if url.text.find(".html") != -1:
            links.append(url.text)

    fetch(links)


def fetch(urls):
    for url in urls:
        nf = urlopen(url)
        start = time.time()
        nf.read()
        end = time.time()
        nf.close()
        print("Warm up: {0}\t\tTime taken: {1} ms".format(url, round((end - start) * 1000)))


def _usage():
    print("Usage: python warmer.py http://example.com/sitemap")


if __name__ == "__main__":
    urlArg = sys.argv[-1]
    if not urlArg.lower().startswith("http"):
        _usage()
        sys.exit(-1)
    main(urlArg)