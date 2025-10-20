HackCamp Data Masking Project

This project was developed during a two-week HackCamp at the University of Salford in collaboration with IRIS Software Group. Our team designed and implemented a data masking solution to improve security and protect sensitive data.

Features:
-Connected to a PostgreSQL database to manage and store sensitive records.
-Applied JSON-based masking rules to anonymise confidential data.
-Produced masked copies of the database for safer development and testing.
-Implemented multiple rule sets (basic, medium, strict) to allow different levels of masking.

Technologies:
-Python
-PostgreSQL
-JSON

Teamwork & Process:
-Worked in a cross-functional Agile team, following iterative development practices.
-Regularly presented progress and refined our solution with feedback from IRIS architect.
-Delivered a final demo to industry professionals, showcasing the complete masking system.

Learning Outcomes:
-Gained experience in tackling real-world data security challenges.
-Improved collaboration and communication through Agile development.
-Learned how to design adaptable rule-based systems for data protection.

How To Run:
This script is designed to fetch data from a PostgreSQL source database, apply masking rules defined in a JSON template, and insert the masked data into a PostgreSQL target database.
This script works by applying rules of masking logic in the script according to what is specified in the JSON files.

You must use command line arguments to interact with this script. Firstly specify Python and call the script, then pass in the connection information to the host and target databases, and then call the template file. 

Use the following format:
python script_name.py <source_host> <source_db> <source_user> <source_password> <source_table> <target_host> <target_db> <target_user> <target_password> <target_table> <template_file>

For example, it might look like this:
 python "C:\Desktop\Projects\script.py" localhost postgres postgres 123 starterdata.source_table localhost target postgres 123 maskeddata.target_table "C:\Desktop\Projects\basic.json"

Run your script in command line in the above format to see "x rows inserted into the database" and it should print the new masked results into terminal. Run a SELECT query on your target table to show the newly masked data.
