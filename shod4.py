import subprocess
import re
import json
import csv
import subprocess
import sqlite3
import random
ip=[]

new_json_input = input("Enter the new JSON configuration: ")

command = "x-ui stop"
process = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("Error executing command:", command)
else:
    print(stdout.decode('utf-8'))
# Open the database file
conn = sqlite3.connect('/etc/x-ui/x-ui.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Construct the SQL query to retrieve the value of xrayTemplateConfig
query = "SELECT value FROM settings WHERE key = 'xrayTemplateConfig'"

# Execute the query and fetch the result 
cursor.execute(query)
result = cursor.fetchone()

# Close the database connection


# Extract the value from the result tuple
if result is not None:
    value = result[0]
    print("The current value of xrayTemplateConfig is:", value)
else:
    print("xrayTemplateConfig not found in the database.")



 # Replace values with user input

    # Try to parse the user-provided JSON
    new_config = json.loads(new_json_input)


query = "UPDATE settings SET value = ? WHERE key = 'xrayTemplateConfig'"

# Execute the query with the new value
cursor.execute(query, (new_config,))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

command = "x-ui start"
process = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("Error executing command:", command)
else:
    print(stdout.decode('utf-8'))
