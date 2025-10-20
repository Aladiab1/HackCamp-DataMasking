Thank you for allowing us to create a data masking tool for IRIS Computing Solutions!
Team members of Group 15:
Product Owner - Luke Slattery
Scrum Master - Trinity Booth
General Developers - Berk Mehmedov, Ala Diab, Salma Aloush, Alex Wilson, Waleed Khalid
Data Architect - Berk Mehmedov
Security Master - Alex Wilson
Documentation and Reporting Specialist - Ala Diab, Salma Aloush
Command Line Interface (CLI) - Waleed Khalid

This script is designed to fetch data from a PostgreSQL source database, apply masking rules defined in a JSON template, and insert the masked data into a PostgreSQL target database.
This script works by applying rules of masking logic in the script according to what is specified in the JSON files.

You must use command line arguments to interact with this script. Firstly specify Python and call the script, then pass in the connection information to the host and target databases, and then call the template file. 

Use the following format:
python script_name.py <source_host> <source_db> <source_user> <source_password> <source_table> <target_host> <target_db> <target_user> <target_password> <target_table> <template_file>

For example, it might look like this:
 python "C:\Desktop\Projects\script.py" localhost postgres postgres 123 starterdata.source_table localhost target postgres 123 maskeddata.target_table "C:\Desktop\Projects\basic.json"

Run your script in command line in the above format to see "x rows inserted into the database" and it should print the new masked results into terminal. Run a SELECT query on your target table to show the newly masked data.
