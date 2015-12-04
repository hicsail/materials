import sys, getopt
import sqlalchemy
import json
from config import config
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from db import Base
from parsers import NistParser
from spiders import NistSpider


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ['get-urls', 'get-listings', 'parse-listings'])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        sys.exit(2)

    # Loop through options and arguments
    for o, a in opts:
        if o == '--get-urls':
            get_urls()
        elif o == '--get-listings':
            get_listings()
        elif o == '--parse-listings':
            # Init db connection
            print sqlalchemy.__version__
            engine = engine_from_config(config, prefix='sqlalchemy.')
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            # Store data in db
            parse_listings(session)
        else:
            assert False, usage()


def get_urls():
    urls = [
        'http://ilthermo.boulder.nist.gov/ILT2/ilsearch?cmp=&ncmp=1&year=&auth=&keyw=&prp=0',
        'http://ilthermo.boulder.nist.gov/ILT2/ilsearch?cmp=&ncmp=2&year=&auth=&keyw=&prp=0',
        'http://ilthermo.boulder.nist.gov/ILT2/ilsearch?cmp=&ncmp=3&year=&auth=&keyw=&prp=0'
    ]
    nist_spider = NistSpider()
    data = nist_spider.get_urls(urls)
    with open('resources/urls.txt', 'w') as f:
        f.write(json.dumps(data))


def get_listings():
    try:
        with open('resources/urls.txt') as f:
            urls = json.loads(f.read())
    except IOError:
        print('Call materials.py with --get-urls first')
        sys.exit(1)
    nist_spider = NistSpider()
    data = nist_spider.get_listings(urls)
    with open('resources/data.txt', 'w') as f:
        f.write(json.dumps(data))


def parse_listings(session):
    try:
        with open('resources/data.txt') as f:
            data = json.loads(f.read())
    except IOError:
        print('Call materials.py with --get-listings first')
        sys.exit(1)
    length = len(data)
    for i in xrange(len(data)):
        print('Parsing data URL %s of %s: %s' % (i+1, length, data[i][0]))
        nist = NistParser(session, data[i][1], data[i][0])
        nist.parse_and_store()


def usage():
    print('$ python materials/materials.py --get-urls --get-listings --parse-listings')
    print('Call from main folder')
    print('Be sure to follow the order of options')

if __name__ == '__main__':
    main()
