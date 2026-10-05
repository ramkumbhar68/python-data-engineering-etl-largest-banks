# Python Project for Data Engineering – Largest Banks ETL

## Description

This project demonstrates a complete **ETL (Extract, Transform, Load) pipeline using Python**.

The pipeline extracts the names and market capitalization of the world's largest banks from a web source, transforms the market capitalization values from USD into **GBP, EUR, and INR** using exchange-rate data, and loads the transformed dataset into both a **CSV file and a SQLite database**. SQL queries are then executed against the database, and each major stage of the pipeline is recorded in a timestamped log file.

This project was developed as a practical **Python for Data Engineering** project and demonstrates core data-engineering concepts such as web data extraction, data transformation, file handling, database loading, SQL querying, and ETL process logging.

## Project Workflow

```text
Web Source
    |
    v
Extract bank names + market capitalization
    |
    v
Transform USD values
    |----> GBP
    |----> EUR
    |----> INR
    |
    v
Load transformed data
    |----> Largest_banks_data.csv
    |----> Banks.db (SQLite)
    |
    v
Run SQL queries
    |
    v
Log ETL execution in code_log.txt
```

## Technologies Used

- **Python 3**
- **Pandas** – data manipulation and CSV processing
- **NumPy** – numerical calculations and rounding
- **Requests** – retrieving web content
- **BeautifulSoup** – HTML parsing and data extraction
- **SQLite** – relational database storage
- **SQL** – querying the loaded dataset
- **Git/GitHub** – source-code version control

## Project Structure

```text
python-data-engineering-etl-largest-banks/
│
├── banks_project.py
├── exchange_rate.csv
├── Largest_banks_data.csv
├── Banks.db
├── code_log.txt
├── requirements.txt
├── .gitignore
└── README.md
```

### File Details

| File | Purpose |
|---|---|
| `banks_project.py` | Main Python ETL pipeline |
| `exchange_rate.csv` | Currency exchange-rate input data |
| `Largest_banks_data.csv` | Final transformed output |
| `Banks.db` | SQLite database containing the `Largest_banks` table |
| `code_log.txt` | Timestamped ETL execution log |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from Git |
| `README.md` | Project documentation |

## ETL Pipeline

### 1. Extract

The `extract()` function retrieves the bank data from the archived Wikipedia page using `Requests` and `BeautifulSoup`.

The extracted fields are:

- Bank name
- Market capitalization in USD billions

The data is stored in a Pandas DataFrame.

### 2. Transform

The `transform()` function reads exchange-rate data and calculates market capitalization in:

- GBP billions
- EUR billions
- INR billions

The transformed values are rounded to two decimal places.

### 3. Load

The final DataFrame is loaded into:

1. `Largest_banks_data.csv`
2. `Banks.db`

The SQLite table is named:

```text
Largest_banks
```

### 4. SQL Analysis

The project executes SQL queries including:

```sql
SELECT * FROM Largest_banks;
```

```sql
SELECT AVG(MC_GBP_Billion) FROM Largest_banks;
```

```sql
SELECT Name FROM Largest_banks LIMIT 5;
```

These queries demonstrate basic analytical querying after the ETL load.

### 5. Logging

The `log_progress()` function records important pipeline stages in `code_log.txt`, including:

- ETL initialization
- Data extraction
- Data transformation
- CSV loading
- Database connection
- Database loading
- SQL query execution
- Process completion
- Database connection closure

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/ramkumbhar68/python-data-engineering-etl-largest-banks.git
cd python-data-engineering-etl-largest-banks
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the ETL pipeline

```bash
python banks_project.py
```

The script will:

- Extract bank information
- Transform market capitalization into multiple currencies
- Generate/update the CSV output
- Load data into SQLite
- Execute SQL queries
- Write execution details to `code_log.txt`

## Key Data Engineering Concepts Demonstrated

- ETL pipeline design
- Web data extraction
- HTML parsing
- DataFrame manipulation
- Currency transformation
- CSV input/output
- Relational database loading
- SQLite database operations
- SQL querying
- Pipeline logging
- Python modular functions

## Data Sources

The project uses:

- An archived Wikipedia page for bank and market-capitalization data.
- IBM Skills Network exchange-rate data for currency conversion.

The web source and exchange-rate source are referenced directly in `banks_project.py`.

## Learning Outcome

This project demonstrates how Python can be used to build a small end-to-end data pipeline—from **extracting raw data to transforming it, storing it in structured formats, and querying the resulting dataset**.

It provides a foundation for progressing toward larger data-engineering technologies such as **SQL, Apache Spark, Hadoop, cloud data lakes, Databricks, and modern ETL/ELT platforms**.

## Author

**Ram Kumbhar**

GitHub: https://github.com/ramkumbhar68
