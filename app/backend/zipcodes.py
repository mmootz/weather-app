"""
load zipcodes for lookup.
"""
import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))
ZIPCODE_DB = os.path.join(current_dir, "data/uszips.csv")


def load_zipcodes(path=ZIPCODE_DB):
    """
    Load zipcodes from static file and return a dict
    """
    zipcodes = {}

    with open(path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            zipcodes[row["zip"]] = (
                float(row["lat"]),
                float(row["lng"]),
            )

    return zipcodes


# Load once at import time
ZIPCODES = load_zipcodes()


def zipcode_lookup(zipcode):
    """
    Takes a zipcode and returns (lat, lon)
    """
    try:
        return ZIPCODES[str(zipcode)]
    except KeyError:
        raise ValueError(f"Invalid ZIP code: {zipcode}")