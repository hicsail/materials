import requests


class NistSpider:

    listing_url_prefix = 'http://ilthermo.boulder.nist.gov/ILT2/ilset?set='

    def __init__(self):
        pass

    @staticmethod
    def get_urls(urls):
        entities = []
        setid = None
        for url in urls:
            print('Getting URL %s' % url)
            r = requests.get(url)
            data = r.json()
            # Check where the setid property is located, defines the URL of the mixture
            for i in xrange(len(data['header'])):
                if data['header'][i] == 'setid':
                    setid = i
                    break
            for entry in data['res']:
                entities.append(NistSpider.listing_url_prefix + entry[setid])
        return entities

    @staticmethod
    def get_listings(urls):
        listings = []
        length = len(urls)
        for i in xrange(len(urls)):
            print('Getting URL %s of %s: %s' % (i+1, length, urls[i]))
            r = requests.get(urls[i])
            data = r.json()
            listings.append((urls[i], data))
        return listings
