import sqlite3
import scrapper
import sys
import pandas as pd
import exchange_rates
from datetime import date


def main():

    if len(sys.argv) == 1:
        print("Usage: python3 main.py <property_type1> <property_type2> ...")
        sys.exit(1)

    # Dict holding exchange rates
    rates = exchange_rates.get_exchange_rates()

    # Properties types to be extracted
    property_types = {}

    # Add property types to the dictionary
    for arg in sys.argv[1:]:
        if arg not in scrapper.property_types:
            print(f"Invalid property type: {arg}")
            sys.exit(1)

        property_types[arg] = scrapper.extract_total_pages()[arg]

    # Extract, clean and add date to data from website
    df = scrapper.extract_data(property_types)
    df = scrapper.data_cleaner(df, UFtoCLP=rates["UF"], USDtoCLP=rates["USD"])
    df["date"] = date.today()

    # Write the data to the database
    conn = sqlite3.connect("properties.db")

    df.to_sql("properties", conn, if_exists="append", index=False)
    conn.close()

    print("Data written to the database")


main()
