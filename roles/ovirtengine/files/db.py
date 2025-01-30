#!/usr/bin/python3

import psycopg2
import json
from psycopg2 import sql

# Function to read database parameters from configuration file
def get_db_params(config_file):
    db_params = {}
    try:
        with open(config_file, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    if key == 'ENGINE_DB_DATABASE':
                        db_params['dbname'] = value
                    elif key == 'ENGINE_DB_USER':
                        db_params['user'] = value
                    elif key == 'ENGINE_DB_PASSWORD':
                        db_params['password'] = value
                    elif key == 'ENGINE_DB_HOST':
                        db_params['host'] = value
                    elif key == 'ENGINE_DB_PORT':
                        db_params['port'] = value
    except Exception as e:
        print(f"Error reading database configuration: {e}")
    return db_params

# Read database parameters from config file
db_params = get_db_params('/etc/ovirt-engine/engine.conf.d/10-setup-database.conf')

# Queries to retrieve data from the specified tables
queries = {
    'public.cluster': "SELECT name AS CLUSTER, cluster_id AS CLUSTER_ID, description AS DESCRIPTION FROM public.cluster;",
    'public.vds_static': "SELECT vds_name AS KVM, vds_id AS VDS_ID, vds_unique_id AS VDS_UNIQ_ID, host_name AS HOST_NAME, cluster_id AS CLUSTER FROM public.vds_static;",
    'public.storage_domain_static': "SELECT storage_name AS STORAGE_NAME, id AS STORAGE_ID, storage AS STORAGE, storage_type AS TYPE, storage_domain_type AS DOMAIN_TYPE FROM public.storage_domain_static;"
}

def fetch_data(query):
    try:
        # Establish a connection to the database
        with psycopg2.connect(**db_params) as conn:
            # Create a cursor object
            with conn.cursor() as cur:
                # Execute the SQL query
                cur.execute(query)
                # Fetch all rows from the executed query
                rows = cur.fetchall()
                # Retrieve column names from the cursor description
                col_names = [desc[0] for desc in cur.description]
                return col_names, rows
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def save_to_json(data, filename="db.json"):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

def main():
    result = {}
    for table, query in queries.items():
        print(f"\nFetching data from {table}...")
        col_names, rows = fetch_data(query)
        if rows:
            result[table] = [dict(zip(col_names, row)) for row in rows]
        else:
            print("No data retrieved or an error occurred.")
    
    save_to_json(result)

if __name__ == "__main__":
    main()
