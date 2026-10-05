# Code for ETL operations on Country-GDP data

# Importing the required libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime


def log_progress(message):
    """
    Logs a timestamped message to code_log.txt.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(logfile, "a") as f:
        f.write(f"{timestamp} : {message}\n")

    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

def extract(url, table_attribs):
    """ Extracts bank names and market capitalization values
    from the table under 'By market capitalization'."""
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    # The table under "By market capitalization" is the first table in the archived webpage.
    table = soup.find_all("tbody")[0]
    df = pd.DataFrame(columns=table_attribs)
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) != 0:
            bank_name = columns[1].get_text(strip=True)
            market_cap = columns[2].get_text()
            # Remove the trailing character, such as '\n',
            # and convert the value to float.
            market_cap = float(market_cap[:-1])
            row_data = {
                "Name": bank_name,
                "MC_USD_Billion": market_cap}
            df = pd.concat(
                [df, pd.DataFrame([row_data])],
                ignore_index=True)
    return df

    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

def transform(df, csv_path):
    """Adds market capitalization values in GBP, EUR, and INR."""
    exchange_rate_df = pd.read_csv(csv_path)
    
    exchange_rate = (exchange_rate_df.set_index("Currency").to_dict()["Rate"])

    # Ensure exchange_rate['GBP'] is always a float
    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])

    df["MC_GBP_Billion"] = [np.round(x * gbp_rate,2) for x in df["MC_USD_Billion"]]

    df["MC_EUR_Billion"] = [np.round(x * eur_rate,2) for x in df["MC_USD_Billion"]]

    df["MC_INR_Billion"] = [np.round(x * inr_rate,2) for x in df["MC_USD_Billion"]]
    return df
    ''' This function accesses the CSV file for exchange rate
	information, and adds three columns to the data frame, each
	containing the transformed version of Market Cap column to
	respective currencies'''

def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    log_progress("Data saved to CSV file")

    ''' This function saves the final data frame as a CSV file in
	the provided path. Function returns nothing.'''

def load_to_db(df, sql_connection, table_name):
    df.to_sql(
        table_name,
        sql_connection,
        if_exists="replace",
        index=False
    )
    log_progress("Data loaded to Database as a table, Executing queries")

    ''' This function saves the final data frame to a database
	table with the provided name. Function returns nothing.'''

def run_query(query_statement, sql_connection):
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_statement)
    print(query_output)
    log_progress(f"Executed query: {query_statement}")

    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''

''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
csv_path = ("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv")
table_attribs = ["Name", "MC_USD_Billion"]
final_table_attribs = [
    "Name",
    "MC_USD_Billion",
    "MC_GBP_Billion",
    "MC_EUR_Billion",
    "MC_INR_Billion", 
    ]
exchange_rate_csv = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
)
output_path = "./Largest_banks_data.csv"
db_name = "Banks.db"
table_name = "Largest_banks"
logfile = "code_log.txt"

log_progress("Preliminaries complete. Initiating ETL process")
df = extract(url, table_attribs)
print(df)
log_progress("Data extraction complete. Initiating Transformation process")
df = transform(df, exchange_rate_csv)
print(df)
print(df["MC_EUR_Billion"][4])
log_progress("Data transformation complete. Initiating Loading process")
load_to_csv(df, output_path)

sql_connection = sqlite3.connect("Banks.db")
log_progress("SQL Connection initiated")
load_to_db(df, sql_connection, table_name)

query_1 = "Select * from Largest_banks"
run_query(query_1, sql_connection)
query_2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query_2, sql_connection)
query_3 = "SELECT Name from Largest_banks LIMIT 5"
run_query(query_3, sql_connection)
log_progress("Process Complete")
sql_connection.close()
log_progress("Server Connection closed")

