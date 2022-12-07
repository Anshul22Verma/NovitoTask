import argparse
import pandas as pd

from db.dbc import DataBaseConnection


def create_value_definition_table(db_file: str) -> None:
    '''
        Create value definition table in the database
        
        :param db_file: (str), path of the SQLite database file
        :return: None
    '''
    # query to create the value-definition table if it does not exist
    query = "CREATE TABLE IF NOT EXISTS value_definition(\
        id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT NOT NULL, type TEXT NOT NULL, metric_id INTEGER NOT NULL, \
        FOREIGN KEY (metric_id)  \
            REFERENCES metric (id) \
    );"

    dbc = DataBaseConnection(db_file=db_file)
    dbc.query(query=query)

    # # delete all records from both the tables if needed
    # query = "DELETE FROM metric WHERE 1=1;"
    # dbc.query(query=query)
    # query = "DELETE FROM value_definition WHERE 1=1;"
    # dbc.query(query=query)

    # commit and close the connection
    dbc.close()
    return

def insert_data_to_db(csv_file: str, db_file: str) -> None:
    '''
        Insert data from csv file into the database

        :param csv_file: (str), path of the CSV file with metadata
        :param db_file: (str), path of the SQLite database file
        :return: None
    '''
    dbc = DataBaseConnection(db_file=db_file)
    df = pd.read_csv(csv_file)

    # first lets insert into the metric table
    metrics_df = df[['metric_code', 'metric_description']].drop_duplicates()
    # values to insert in mertrics table
    metrics_insert = list(zip(metrics_df['metric_code'], metrics_df['metric_description']))
    ids = {}
    for metric_val in metrics_insert:
        metric_code, metric_desc = metric_val

        # make sure that the code does not exist (NOT NEEDED unique column in table)
        query = f"SELECT id FROM metric WHERE code='{metric_code}'"
        if len(dbc.query(query=query)) < 1:
            # insert into metric table
            query = f"INSERT INTO metric(code,description) VALUES('{metric_code}','{metric_desc}');"
            dbc.query(query=query)

        # get the id of these rows for them to be foriegn key of the value table
        query = f"SELECT id FROM metric WHERE code='{metric_code}'"
        ids[metric_code] = dbc.query(query=query)[0][0]

    # insert into values_defintion table
    for _, row in df.iterrows():
        query = f"INSERT INTO value_definition(metric_id,label,type) VALUES('{ids[row['metric_code']]}','{row['value_label']}','{row['value_type']}');"
        dbc.query(query=query)
    
    # commit and close the connection
    dbc.close()
    return

def show_tables(db_file: str) -> None:
    '''
        Prints the table for preview

        :param db_file: (str), path of the SQLite database file
        :return: None
    '''
    dbc = DataBaseConnection(db_file=db_file)
    print("-"*10 + " "*3 + "Table after insert" + " "*3 + "-"*10)
    print("\n")
    query = "SELECT * FROM metric;"
    result = dbc.query(query=query)
    print("-"*10 + " "*5 + "Table metric" + " "*5 + "-"*10)
    print("[id, code, description]")
    for idx, r in enumerate(result):
        print(f"row {idx+1}: ", r)
    
    print("\n")
    query = "SELECT * FROM value_definition;"
    result = dbc.query(query=query)
    print("-"*10 + " "*5 + "Table value_definition" + " "*5 + "-"*10)
    print("[id, label, type, metric_id]")
    for idx, r in enumerate(result):
        print(f"row {idx+1}: ", r)

    # commit and close the connection
    dbc.close()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input Variables')
    parser.add_argument("--db_file", type=str, default='./db/test.db', \
        required=False, help="SQLite3 DataBase file path")
    parser.add_argument("--csv_file", type=str, default='./resources/metrics.csv', \
        required=False, help="csv file path with metadata to be inserted in the DB")
    args = parser.parse_args()

    # creates the value definition table in the database
    create_value_definition_table(db_file=args.db_file)

    # add data from python file to the table
    insert_data_to_db(csv_file=args.csv_file, db_file=args.db_file)

    # show the changes
    show_tables(db_file=args.db_file)
