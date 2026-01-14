import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))

ZIPCODES = {}

zipcodedb = os.path.join(current_dir, "data/uszips.csv")
def load_zipcodes(path=zipcodedb):
    """
    load zipcodes from static file
    """
    global ZIPCODES
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            ZIPCODES[row["zip"]] = (
                float(row["lat"]),
                float(row["lng"]),
            )


def zipcode_lookup(zipcode):
    """
    Docstring for zipcode_lookup
    takes a zipcode and returns lat and log
    """
    try:
        return ZIPCODES[str(zipcode)]
    except KeyError:
        raise ValueError(f"Invalid ZIP code: {zipcode}")
