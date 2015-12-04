# Materials
A scraper for the NIST Ionic Liquids Database.

## Usage
Tested with Python 2.7.10 and PostgreSQL 9.4.5.

Create config.py from config.example.py. Run `$ pip install -r requirements.txt`. Then from the main folder, run
`$ python materials/materials.py --get-urls --get-listings --parse-listings`. These three options can be run separately
but depend on each other.
