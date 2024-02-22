import sqlite3
import scrapper
import sys
import pandas as pd
import exchange_rates
from datetime import date
import csv


db = "properties.db"

def main():

    if len(sys.argv) == 1:
        print("Usage: python3 main.py <command_order> <property_type1> <property_type2> ...")
        sys.exit(1)


    # Extraction part
    if sys.argv[1] == "-extract":

        # Dict holding exchange rates
        rates = exchange_rates.get_exchange_rates()

        # Properties types to be extracted
        property_types = {}

        # Add property types to the dictionary
        for arg in sys.argv[2:]:
            if arg not in scrapper.property_types:
                print(f"Invalid property type: {arg}")
                sys.exit(1)

            property_types[arg] = scrapper.extract_total_pages()[arg]

        # Extract, clean and add date to data from website
        df = scrapper.extract_data(property_types)
        df = scrapper.data_cleaner(df, UFtoCLP=rates["UF"], USDtoCLP=rates["USD"])
        df["date"] = date.today()

        # Write the data to the database
        conn = sqlite3.connect(db)

        df.to_sql("properties", conn, if_exists="append", index=False)
        conn.close()

        print("Data written to the database")

    # Save data from db into csv
    elif sys.argv[1] == "-csv":

        if len(sys.argv) != 2:
            print("Usage: python3 main.py -csv <YYYY-MM-DD>")
            sys.exit(1)

        req_date = sys.argv[2]
        
        conn = sqlite3.connect("properties.db")

        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM properties WHERE date = '{req_date}'")

        rows = cursor.fetchall()

        columns = (description[0] for description in cursor.description)

        if rows == []:
            print(f"No data for {req_date}")
            conn.close()
            sys.exit(1)

        with open(f"extractions/{req_date}properties.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(rows)

        conn.close()



main()
