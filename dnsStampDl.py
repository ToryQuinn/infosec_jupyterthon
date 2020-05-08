import requests
import dnsstamps
from bs4 import BeautifulSoup

def parseDnsStampFromUrl(url):
    r = requests.get(url)
    stamps = filter(lambda x: x.startswith('sdns://'),r.text.splitlines())
    parsed_stamps = list(map(dnsstamps.parse, stamps))
    domains = filter(None, map(lambda x: x.hostname, parsed_stamps))
    ips = filter(None, map(lambda x: x.address, parsed_stamps))
    return {'domains': list(domains),'ips': list(ips) }

def getDnsStampFileUrls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    hrefs = map(lambda x: x.get('href'),soup.find_all('a'))
    md_files = filter(lambda x: x.endswith('.md'), hrefs)
    return map(lambda x: url + x, md_files)

def massageString(s):
    return s.replace('[','').split(']')[0] if s.startswith('[') else s.split(':')[0]

def sumStamps(stamps):
    domains = sum((list(map(massageString,x['domains'])) for x in stamps),[])
    ips = sum((list(map(massageString,x['ips'])) for x in stamps),[])
    return {'domains': set(domains), 'ips': set(ips)}

def main():
    url = "https://download.dnscrypt.info/dnscrypt-resolvers/v2/"
    urls = getDnsStampFileUrls(url)
    stamps = list(map(parseDnsStampFromUrl,urls))
    results = sumStamps(stamps)
    with open('ips.txt','w') as f:
        f.writelines('\n'.join(results['ips']))
    with open('domains.txt','w') as f:
        f.writelines('\n'.join(results['domains']))

if __name__ == '__main__':
    main()
