import duckdb
import pandas as pd
import pyarrow as pa
import os

if __name__ == '__main__':
    # Connect to a persistent DuckDB database file
    conn = duckdb.connect(database='demo.db', read_only=False)
    cur = conn.cursor()

    cur.execute("CREATE SEQUENCE seq")
    cur.execute("CREATE TABLE modesearch (id BIGINT DEFAULT NEXTVAL('seq'), antecedent STRING, consequent STRING, confidence FLOAT, lift FLOAT, support FLOAT)")

    file_base = "./output/"
    file_names = os.listdir(file_base)

    for file_name in file_names:
        filename = file_base + file_name
        print('Now processing file:', filename)
        cur.execute("INSERT INTO modesearch (antecedent, consequent, confidence, lift, support) SELECT * FROM read_csv_auto(' + filename + ')")

    conn.close()
