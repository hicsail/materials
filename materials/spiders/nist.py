import requests


class NistSpider:

    urls = [
        'http://ilthermo.boulder.nist.gov/ILT2/ilsearch?cmp=&ncmp=1&year=&auth=&keyw=&prp=0',
        'http://ilthermo.boulder.nist.gov/ILT2/ilsearch?cmp=&ncmp=2&year=&auth=&keyw=&prp=0',
        'http://ilthermo.boulder.nist.gov/ILT2/ilsearch?cmp=&ncmp=3&year=&auth=&keyw=&prp=0'
    ]

    listing_url_prefix = 'http://ilthermo.boulder.nist.gov/ILT2/ilset?set='

    def __init__(self):
        pass

    @staticmethod
    def parse():
        entities = []
        setid = None
        for url in NistSpider.urls:
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
