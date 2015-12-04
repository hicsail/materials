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
        # Get CLI options
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
            print('SQLAlchemy version' + sqlalchemy.__version__)
            engine = engine_from_config(config, prefix='sqlalchemy.')
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            # Store data in db
            parse_listings(session)
        else:
            assert False, usage()


def get_urls():
    """
    Runs sequence of searches on NIST website which return all mixtures. Writes list of URLs to resources/urls.txt.
    """
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
    """
    Executes request for each individual URL and stores result in resources/data.txt.
    """
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
    """
    Parses listing data and stores entries in database.
    :param session: Database session
    """
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
    print('Usage: $ python materials/materials.py --get-urls --get-listings --parse-listings')
    print('--get-urls writes list of all URLs to the resources folder')
    print('--get-listings uses the list of URLs and stores output in the resources folder')
    print('--parse-listings takes the listing data and stores it in the db')
    print('The order of these 3 commands matters.')
    print('Set any options for SQLAlchemy in config.py')

if __name__ == '__main__':
    main()
