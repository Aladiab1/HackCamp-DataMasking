import psycopg2
import json
import os
import argparse

# Load the JSON template for masking (asks user for the path)
def load_masking_template(template_path):
    try:
        # Check if the file exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"The template file '{template_path}' does not exist.")

        # Open and load the JSON template
        with open(template_path, "r") as file:
            return json.load(file)
    except Exception as error:
        print(f"Error loading JSON template: {error}")
        return {}


# Data Masking Function
def mask_data(data, column_names, masking_rules):
    print(f"Applying masking rules from template: {masking_rules}")
    masked_data = []

    # Iterate over each record in the fetched data
    for record in data:
        masked_record = {}

        # Iterate over each column in the record
        for idx, column_name in enumerate(column_names):
            print(f"Processing column: {column_name}")  # Add this line to log column names
            if column_name in masking_rules:
                rule = masking_rules[column_name]

                # Apply the masking based on the rule type
                if rule["maskingType"] == "redact":
                    masked_record[column_name] = rule["replacement"]
                elif rule["maskingType"] == "partial":
                    replacement = rule.get("replacement", "*")
                    if column_name == "email":
                        # Updated email masking logic
                        at_index = record[idx].find('@')
                        if at_index != -1:
                            masked_record[column_name] = record[idx][:at_index] + '****' + record[idx][at_index:]
                        else:
                            masked_record[column_name] = '****'
                    elif column_name == "ssn":
                        # Mask SSN (e.g., last 4 digits remain visible)
                        masked_record[column_name] = rule["replacement"] + record[idx][-4:]
                    else:
                        # Mask other columns partially
                        masked_record[column_name] = record[idx][:len(record[idx])//2] + rule["replacement"]
                elif rule["maskingType"] == "last_4":
                    # Show only the last 4 digits (e.g., for SSN)
                    masked_record[column_name] = rule["replacement"] + record[idx][-4:]
                else:
                    # No specific masking rule for this column; leave the original data
                    masked_record[column_name] = record[idx]
            else:
                # No rule for this column, keep the original data
                masked_record[column_name] = record[idx]

        print(f"Masked record: {masked_record}")  # Add this line to log masked data
        # Append the masked record to the final list
        masked_data.append(masked_record)

    return masked_data


# Function to fetch data from the source PostgreSQL database
def fetch_data_from_db(host, db_name, user, password, table_name):
    connection = None
    cursor = None
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            database=db_name,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        # Fetch data from the specified table
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)

        # Fetch all rows and column names
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        return rows, column_names

    except Exception as error:
        print(f"Error fetching data from source database: {error}")
        return [], []

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Function to insert masked data into the target PostgreSQL database
def insert_data_to_db(host, db_name, user, password, table_name, data, column_names):
    connection = None
    cursor = None
    try:
        # Connect to the PostgreSQL target database
        connection = psycopg2.connect(
            host=host,
            database=db_name,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        # Prepare the INSERT query
        columns = ", ".join(column_names)
        placeholders = ", ".join(["%s"] * len(column_names))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Insert each masked record into the target table
        for record in data:
            values = [record[col] for col in column_names]
            cursor.execute(query, values)

        connection.commit()
        print(f"Inserted {len(data)} rows into the target database.")

    except Exception as error:
        print(f"Error inserting data into target database: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Main function that handles user input and runs the process
def main():
    # Command-line arguments to get database credentials, table names, and template file
    parser = argparse.ArgumentParser(description="Mask data from source to target database using JSON templates")
    parser.add_argument("source_host", help="Host of the source PostgreSQL server")
    parser.add_argument("source_db", help="Source database name")
    parser.add_argument("source_user", help="Username for the source database")
    parser.add_argument("source_password", help="Password for the source database")
    parser.add_argument("source_table", help="Table name in the source database")
    parser.add_argument("target_host", help="Host of the target PostgreSQL server")
    parser.add_argument("target_db", help="Target database name")
    parser.add_argument("target_user", help="Username for the target database")
    parser.add_argument("target_password", help="Password for the target database")
    parser.add_argument("target_table", help="Table name in the target database")
    parser.add_argument("template_file", help="Path to the JSON masking template file")

    # Parse the arguments
    args = parser.parse_args()

    # Load the masking template specified by the user
    masking_template = load_masking_template(args.template_file)
    if not masking_template or "fields" not in masking_template:
        print("Invalid or missing masking template.")
        return

    # Fetch data from the source database
    source_data, column_names = fetch_data_from_db(
        args.source_host, args.source_db, args.source_user, args.source_password, args.source_table
    )

    if source_data:
        print(f"Retrieved {len(source_data)} rows from the source table '{args.source_table}'.")

        # Apply masking to the data based on the template
        masked_data = mask_data(source_data, column_names, masking_template["fields"])

        # Insert the masked data into the target database
        insert_data_to_db(
            args.target_host, args.target_db, args.target_user, args.target_password, args.target_table, masked_data, column_names
        )
    else:
        print("No data retrieved from source database.")


if __name__ == "__main__":
    main()
