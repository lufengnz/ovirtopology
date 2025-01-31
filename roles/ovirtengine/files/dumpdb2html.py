#!/usr/bin/python3

import psycopg2
import os
from psycopg2 import sql

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

db_params = get_db_params('/etc/ovirt-engine/engine.conf.d/10-setup-database.conf')

queries = {
    'public.cluster': "SELECT name AS CLUSTER, cluster_id AS CLUSTER_ID, description AS DESCRIPTION FROM public.cluster;",
    'public.vds_static': "SELECT vds_name AS KVM, vds_id AS VDS_ID, vds_unique_id AS VDS_UNIQ_ID, host_name AS HOST_NAME, cluster_id AS CLUSTER FROM public.vds_static;",
    'public.storage_domain_static': "SELECT storage_name AS STORAGE_NAME, id AS STORAGE_ID, storage AS STORAGE, storage_type AS TYPE, storage_domain_type AS DOMAIN_TYPE FROM public.storage_domain_static;"
}

def fetch_data(query):
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                col_names = [desc[0] for desc in cur.description]
                return col_names, rows
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def save_to_html(data, filename="db_output.html"):
    try:
        with open(filename, "w") as html_file:
            html_file.write("<html><head><title>Database Output</title></head><body>\n")
            html_file.write("<h1>Database Query Results</h1>\n")
            
            for table, rows in data.items():
                html_file.write(f"<h2>Table: {table}</h2>\n")
                html_file.write("<table border='1'><tr>")
                
                headers = rows[0].keys() if rows else []
                for header in headers:
                    html_file.write(f"<th>{header}</th>")
                html_file.write("</tr>\n")
                
                for row in rows:
                    html_file.write("<tr>")
                    for value in row.values():
                        html_file.write(f"<td>{value}</td>")
                    html_file.write("</tr>\n")
                
                html_file.write("</table><br><br>\n")
            
            html_file.write("</body></html>\n")
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to HTML: {e}")

def main():
    result = {}
    for table, query in queries.items():
        print(f"\nFetching data from {table}...")
        col_names, rows = fetch_data(query)
        if rows:
            result[table] = [dict(zip(col_names, row)) for row in rows]
        else:
            print("No data retrieved or an error occurred.")
    
    save_to_html(result)

if __name__ == "__main__":
    main()
